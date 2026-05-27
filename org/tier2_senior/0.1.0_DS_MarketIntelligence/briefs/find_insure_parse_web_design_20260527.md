# FIND_INSURE Phase 1 parse-web Lambda — design brief (DS ~A pre-TO scaffold)

**Author:** 0.1.0_DS_MarketIntelligence~A
**Date:** 2026-05-27T~16:55Z (v0.1) / 2026-05-27T~17:05Z (v0.2 — CTO arch-input absorption)
**Status:** STANDBY-PREP scaffold — pre-TO substrate work; integrates ws CTO FIND_INSURE.005 ACs at TO-drop
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 + §4 Phase 1 deliverable 2
**Allocation anchor:** `org/tier1_exec/2.0.0_SA_COO/briefs/allocation_20260527T1647Z_find_insure_peak_priority.md`
**Spawn directive:** MSTR SPAWN-WITH-DIRECTION 2026-05-27T16:49Z per Andrew sovereign 16:46Z peak-priority
**Arch-input absorbed:** ws CTO `[ACK + ARCH-INPUT]` 2026-05-27T~17:02Z — 4 hints feeding ws COO FIND_INSURE.005 authoring (BeautifulSoup canonical + per-page url-hash key schema + Rule-17 preserve-all reinforcement + blocked-page minimal-record audit-trail)

---

## 1. Lambda contract

| Dim | Value |
|---|---|
| **Lambda name** | `find-insure-parse-web` (TBD: confirm ws CTO TO naming) |
| **Source path** | `data/find/imo/scripts/silver/web-scrape/parse_web.py` (medallion convention per PRD v0.3 §3.2) |
| **Trigger** | EventBridge per-IMO fan-out post-`crawl-web` bronze completion (Phase 1 §3.6) |
| **Input** | `s3://opal-data-imo/corp/{slug}/bronze/web-scrape/{run-date}/**` — raw HTML payloads + per-page response metadata + sitemap.json + robots.txt + run-metadata.json (exact schema per FIND_INSURE.004 ACs) |
| **Output** | `s3://opal-data-imo/corp/{slug}/silver/web-scrape/{run-date}/` — structured per-page records (page-text + link-graph + title + meta + headings + structured contact-blocks) |
| **Slug source** | Derived from upstream extract_source_list → propagated through crawl-web → received via EventBridge event or via path-walk of bronze prefix. Slug-stability via `data/find/imo/scripts/_util/slugify.py` (Phase 0 single-source-of-truth) |
| **IAM** | `find-insure-lambda-role` (FIND_INSURE.001) — S3 Get/List on bronze; PutObject on silver; CloudWatch Logs; telemetry/ append per PRD §3.5 |
| **Runtime** | Python 3.11 Lambda (NOT 3.9; new bucket + new pipeline = use current default; falls back to 3.9 only if existing layer pin requires it — confirm with AE at TO-drop) |
| **Memory + timeout** | TBD per CLAUDE.md Rule 5; provisional: 1024 MB / 5 min (HTML parse is CPU + memory-bound on multi-page sites; revisit at ship per empirical) |

---

## 2. Silver-tier output schema (provisional)

Per CLAUDE.md Rule 17: silver = clean shape + preserved content. HTML→JSON parse is genuinely structure-extraction (raw HTML is unstructured payload; silver gives it queryable shape). NO field-slimming, NO fillna with business defaults, NO row-filtering by business semantic — page-content from bronze MUST be preserved.

### 2.1 Per-page structured record (v0.2 — aligned to ws CTO arch-input hint #2)

One file per crawled page at `silver/web-scrape/{slug}/{run-date}/{url_hash}.json` (flat, no `pages/` subdir; `url_hash` = `sha256(url)[:16]`):

```json
{
  "url": "https://example-imo.com/about",
  "url_hash": "a1b2c3d4e5f60718",
  "fetched_at": "2026-05-30T14:22:11Z",
  "http_status": 200,
  "content_type": "text/html; charset=utf-8",
  "etag": "...",
  "last_modified": "...",
  "bronze_key": "corp/example-imo/bronze/web-scrape/2026-05-30/{url_hash}.html",
  "content_hash": "f0e1d2c3b4a59687",
  "page_text": "...full preserved page text (BeautifulSoup .get_text)...",
  "title": "About Us — Example IMO",
  "meta_tags": {
    "description": "Example IMO is a leading insurance marketing organization...",
    "keywords": "insurance, annuity",
    "og:title": "About Us — Example IMO",
    "og:description": "...",
    "og:image": "...",
    "og:site_name": "...",
    "twitter:card": "summary_large_image",
    "canonical": "https://example-imo.com/about",
    "lang": "en",
    "...": "ALL other <meta> name|property attrs preserved (Rule 17 — no whitelist)"
  },
  "headings": {
    "h1": ["About Us"],
    "h2": ["Our Mission", "Leadership Team"],
    "h3": ["Investment Philosophy", "Asset Management Division"],
    "h4": [],
    "h5": [],
    "h6": []
  },
  "links_internal": [
    {"href": "/leadership", "absolute_url": "https://example-imo.com/leadership", "anchor_text": "Meet our leadership", "rel": null}
  ],
  "links_external": [
    {"href": "https://linkedin.com/company/example-imo", "absolute_url": "https://linkedin.com/company/example-imo", "anchor_text": "LinkedIn", "rel": "noopener"}
  ],
  "contact_blocks": {
    "addresses": [
      {"raw_text": "123 Main St, Springfield, IL 62701", "source": "address-tag"}
    ],
    "emails": [
      {"href": "mailto:info@example-imo.com", "anchor_text": "Contact us", "email": "info@example-imo.com"}
    ],
    "phones": [
      {"href": "tel:+18005551234", "anchor_text": "Call 800-555-1234", "phone_raw": "+18005551234"}
    ]
  },
  "structured_data": {
    "json_ld": [],
    "schema_org": []
  }
}
```

**Blocked-page minimal record (per CTO arch-input hint #4 — audit-trail discipline):**

When bronze metadata indicates fetch was 4xx/429/blocked-by-robots, silver writes the minimal record at the same `{url_hash}.json` key — NEVER skip silently:

```json
{
  "url": "https://example-imo.com/private-leadership",
  "url_hash": "9f8e7d6c5b4a3210",
  "fetched_at": "2026-05-30T14:22:18Z",
  "http_status": 403,
  "page_text": null,
  "blocked_reason": "robots",
  "bronze_key": "corp/example-imo/bronze/web-scrape/2026-05-30/{url_hash}.html"
}
```

`blocked_reason` enum: `"robots"` | `"rate-limit"` (429) | `"http_4xx"` | `"http_5xx"` | `"non-html"` (content-type not text/html). Preserves the audit trail required by PRD §9 Q5 robots.txt discipline.

### 2.2 Per-site rollup

One file per IMO at `silver/web-scrape/{slug}/{run-date}/site_index.json`:

```json
{
  "slug": "example-imo",
  "company_name": "Example IMO",
  "run_date": "2026-05-30",
  "parsed_at": "2026-05-30T14:30:00Z",
  "page_count": {
    "crawled": 47,
    "parsed": 45,
    "skipped_non_html": 2,
    "parse_errors": 0
  },
  "link_graph_summary": {
    "internal_edges": 312,
    "external_domains": ["linkedin.com", "facebook.com", "twitter.com"],
    "mailto_unique_count": 3,
    "tel_unique_count": 2
  },
  "page_inventory": [
    {"url": "...", "title": "...", "bronze_key": "...", "silver_key": "..."}
  ]
}
```

### 2.3 Parse-error / skip log

Append-only `silver/web-scrape/{slug}/{run-date}/parse_errors.ndjson` — one line per page-level failure (preserves provenance per Rule 17 spirit; no business-filter drops):

```ndjson
{"bronze_key": "corp/example-imo/bronze/web-scrape/2026-05-30/pages/xyz.html", "error_class": "BeautifulSoup-error", "error_detail": "...", "occurred_at": "..."}
```

---

## 3. Extraction algorithm

### 3.1 Per-page parse stages (v0.2 — BeautifulSoup canonical per CTO hint #1)

```
bronze HTML payload + per-page response metadata
  → if bronze metadata flags blocked (http_status >= 400 OR robots-disallow): write blocked minimal record + skip parse
  → else BeautifulSoup(html, "lxml") parse  [lxml is BS parser-backend, NOT a separate library surface]
  → 1. extract <title>, ALL <meta> tags by name+property (no whitelist; Rule 17 preserve-all per CTO hint #3),
       <link rel="canonical">, JSON-LD <script type="application/ld+json">, OG/Twitter property meta
  → 2. extract headings h1-h6 preserving outline order, ALL of them (Rule 17 preserve-all per CTO hint #3)
  → 3. extract link graph: every <a href> → classify internal vs external by urlparse netloc compare to page url;
       resolve relative hrefs to absolute via urljoin; preserve every link (no host-filter beyond split per CTO hint #3)
  → 4. extract contact blocks: <address> tag raw_text; <a href="mailto:..."> + <a href="tel:..."> anchors;
       fallback regex-find emails + phones in page text. NO dedupe at silver — gold consolidates (per CTO hint #3).
  → 5. extract page_text via BeautifulSoup .get_text(separator=" ", strip=True) — fabric-canonical full-text
       preservation; gold (.006 score-web) does any boilerplate-removal scoring
  → 6. compute content_hash = sha256(raw_html)[:16] — enables Phase 1 re-run change-detection
  → emit per-page record JSON to silver/web-scrape/{slug}/{run-date}/{url_hash}.json
```

### 3.2 Library shortlist (v0.2 — BeautifulSoup canonical per CTO hint #1)

| Library | Use | Layer status |
|---|---|---|
| `beautifulsoup4` | Primary HTML parse — canonical fabric choice (matches `extract_source_list.py` `afe8ddce2`) | Existing Lambda layer per FIND_INSURE.002 AC1 hint |
| `lxml` | BS parser backend (`BeautifulSoup(html, "lxml")`) for perf; NOT used as standalone parser | Existing layer (BS dependency) |
| Standard lib | `urllib.parse` (internal/external classification via netloc compare + relative→absolute), `re`, `json`, `hashlib`, `datetime`, `boto3` | Always available |
| ~~`trafilatura`~~ | ~~Boilerplate removal~~ | DROPPED v0.2 — BeautifulSoup `.get_text()` preserves full text; boilerplate-removal is gold-tier concern (per CTO hint #3: "DO NOT classify or score at silver") |
| ~~`tldextract`~~ | ~~Domain-class detection~~ | DROPPED v0.2 — `urllib.parse.urlparse().netloc` is sufficient for internal/external split |
| ~~`phonenumbers`~~ | ~~Phone normalization~~ | DROPPED v0.2 — silver preserves raw `tel:` hrefs; normalization is gold's job |

**Lambda layer discipline per CLAUDE.md Rule 3:** zero new layer dependencies in v0.2 design. All requirements satisfied by the existing layer that already ships BeautifulSoup4 + lxml + requests for `extract_source_list.py`. No layer-amend ask to AE 0.7 needed at .005 ship — clean dependency posture per fabric-canonical pattern.

### 3.3 Per-IMO fan-out vs per-page fan-out

| Pattern | Pro | Con |
|---|---|---|
| **Per-IMO Lambda** (one invocation per slug; iterates pages within) | Simple invocation graph; one EventBridge fan-out from .004 ; lower invocation-count cost | Memory/time scaling risk if IMO has 100+ pages; possible 15-min Lambda ceiling on multi-100-page sites |
| **Per-page Lambda** (one invocation per page; fan-out via SQS or S3 ObjectCreated trigger) | Better parallelism + isolation per failure | More invocations + more orchestration complexity at Phase 1 scope |

**Default proposal:** per-IMO Lambda v0.1 (PRD §3.3 "prefer Lambda for fetch + parse stages, bounded payload, parallelizable per company"). Each IMO's page set typically 10-50 pages from a politely-rate-limited crawl; falls inside 1024MB/5min budget. If empirically blown for any IMO, escalate to per-page fan-out as a .005-followup TO.

### 3.4 Edge cases (v0.2 — CTO arch-input hint #4 absorbed)

| Edge case | Handling |
|---|---|
| JS-only SPA (ala Phase 0 source page) | BeautifulSoup will yield very short `page_text`; record full meta + headings (often empty); `page_text` is preserved as-is (don't fabricate; Rule 17). Future v0.2 headless-browser layer is a separate scope. No skip-silently. |
| Broken/malformed HTML | lxml backend's recovery mode tolerates most malformed input; on rare BS exception, write minimal record with `blocked_reason: "parse-error"` + preserve raw_html in bronze; no skip-silently. |
| Non-HTML content (PDF, image, redirect) | Write minimal record with `blocked_reason: "non-html"` + content_type preserved + page_text=null; bronze key retained. |
| Unicode encoding (latin-1, gbk, etc.) | Honor `content_type` charset header from bronze metadata; fall back to BeautifulSoup auto-detect; emit page_text as UTF-8 in silver JSON. |
| Multi-page sites with link cycles | url_hash is sha256(url)[:16] — same url = same silver key = silver-side dedup is path-based by construction (per-page silver write is idempotent); link graph in each per-page record is unconstrained (Rule 17 preserve-all). |
| Pages without title / meta / headings | All fields null-allowed; empty arrays preserved; do not fabricate. |
| **Bronze-flagged blocked pages (4xx / 429 / robots-deny)** | **Per CTO arch-input hint #4: silver writes the minimal blocked-record at `{url_hash}.json` with `blocked_reason` enum (`"robots"` / `"rate-limit"` / `"http_4xx"` / `"http_5xx"` / `"non-html"`) — NEVER skip silently. Audit-trail discipline binds PRD §9 Q5 robots.txt honor at silver layer.** |
| Bronze upstream empty | `[BLOCKED-ASK]` to ws COO per §4.3 below — peer-resource class. |

---

## 4. Failure semantics + observability

### 4.1 Telemetry (PRD §3.2 telemetry/ prefix)

Per-Lambda-run record written to `s3://opal-data-imo/telemetry/find-insure-parse-web/{run-date}/{run-id}.ndjson`:

```ndjson
{"run_id": "...", "slug": "...", "started_at": "...", "ended_at": "...", "pages_in": 47, "pages_out": 45, "parse_errors": 0, "skipped_non_html": 2, "lambda_memory_max_mb": 612, "lambda_duration_ms": 18420, "exit_class": "ok"}
```

### 4.2 Idempotence

Re-run same `(slug, run-date)` overwrites the same silver path per PRD §3.2 re-run semantics ("append-by-date; same-day re-runs overwrite same-date paths"). No accidental-delete protection needed at parse-tier (bucket versioning is the backstop).

### 4.3 Failure classes routed to lane COO via [BLOCKED-ASK]

| Class | Trigger | Route |
|---|---|---|
| `bronze-empty` | crawl-web wrote silver-trigger with no bronze HTML for an IMO | `[BLOCKED-ASK] FIND_INSURE.005 — bronze upstream empty for slug={s}` to ws COO; suggested unblocker = `peer-resource` (AE 0.7 .004 re-run or investigation) |
| ~~`layer-missing`~~ | ~~trafilatura/tldextract layer~~ | **DROPPED v0.2** — BeautifulSoup canonical eliminates new layer dependency per CTO hint #1 |
| `iam-deny` | s3:PutObject denied on silver/web-scrape/ | `[BLOCKED-ASK]` to ws COO; suggested unblocker = `operational` (AE 0.7 .001 IAM policy gap per PRD §3.5) |
| `schema-divergence` | crawl-web .004 bronze schema diverges from my assumption in §1 above | `[BLOCKED-ASK] FIND_INSURE.005 — bronze schema contract mismatch` to ws COO; suggested unblocker = `architectural` (ws CTO/CVO) |

---

## 5. Compliance with CLAUDE.md non-negotiables

| Rule | Compliance |
|---|---|
| Rule 3 (deps in layers, not vendored) | trafilatura/tldextract layer amend route to AE at TO-drop |
| Rule 4 (lambda-source-map entry) | Add `find-insure-parse-web` to `infra/aws/lambda/ci/lambda-source-map.json` at ship |
| Rule 5 (Memory + timeout sized) | 1024 MB / 5 min provisional; revisit empirically |
| Rule 6 (Tag after deploy) | `find-insure-parse-web-v{X.Y.Z}` post-apply tag |
| Rule 13 (DS owns commit→QA-deploy) | `data/find/imo/scripts/silver/web-scrape/parse_web.py` falls under DS cycle (silver-tier Python script); use `.tools/safe-deploy.sh` per Rule 13 once code lands AND bronze upstream + bucket land |
| Rule 14 (pre-commit gate) | `.tools/ds-commit-gate.sh data/find/imo/scripts/silver/web-scrape/parse_web.py` clean before stage |
| Rule 14a (safe-commit) | `.tools/safe-commit.sh --author "0.1.0_DS_MarketIntelligence~A <0.1.0_DS_MarketIntelligence~A@opal.agent>" -m "..." -- data/find/imo/scripts/silver/web-scrape/parse_web.py ...` scope-bound |
| Rule 15 (`from __future__ import annotations` first import) | YES — mandatory; gate-enforced |
| Rule 17 (silver scope) | Silver-tier parse is structure-extraction, not field-slimming. HTML→JSON shape extraction preserves ALL bronze content; no business-rule filtering. |
| `no emojis in code` | Plain ASCII prefixes (`OK:`/`WARN:`/`ERROR:`/`SKIP:`) only |

---

## 6. Open questions — RESOLVED (v0.2) + remaining for ws COO at .005 TO authoring

CTO arch-input 17:02Z resolved questions 2 + 4 directly; remaining are COO TO-authoring scope per CTO "No CTO ratify needed post-COO authoring — fabric-aligned library + schema + Rule-17 discipline = autonomous COO FIX-class authority":

| # | Question | Status |
|---|---|---|
| 1 | **Lambda runtime pin** — Python 3.11 vs 3.9 | OPEN for COO. Recommend 3.11 (new pipeline; clean slate); fall back to 3.9 only if existing find-insure layer is 3.9-pinned per AE 0.7. |
| 2 | ~~Library pin: trafilatura vs readability-lxml vs BeautifulSoup~~ | **RESOLVED CTO arch-input #1 — BeautifulSoup canonical with lxml backend.** trafilatura/readability-lxml/tldextract/phonenumbers all dropped from design. |
| 3 | **Per-IMO vs per-page Lambda invocation** — §3.3 default proposal is per-IMO. | OPEN for COO. Recommend per-IMO v0.1; per-page only if empirical 15-min Lambda ceiling blown. |
| 4 | ~~Output partition format — sha1 vs url-slug~~ | **RESOLVED CTO arch-input #2 — `url_hash = sha256(url)[:16]` keyed flat under `silver/web-scrape/{slug}/{run-date}/{url_hash}.json`.** No `pages/` subdir; flat layout. |
| 5 | **Trigger mechanism** — EventBridge from .004 vs S3 ObjectCreated | OPEN for COO. PRD §3.6 default = EventBridge. |
| 6 | **Stage 1 single-IMO smoke vs full-100 sweep** | OPEN for COO. Recommend smoke-first then full-100. |
| 7 | **`site_index.json` rollup** — keep per-IMO rollup (§2.2) given per-page flat layout per CTO hint #2? | NEW question. Recommend KEEP site_index.json as separate flat-layout-sibling — useful for Phase 3 join discovery + telemetry rollup; doesn't violate CTO's per-page-not-per-IMO-aggregate guidance because site_index is metadata/inventory, not content-aggregate. Route to COO for ratify-or-drop. |

---

## 7. RAVC2-Request shape (for when .005 closes)

```
[RAVC2-Request] FIND_INSURE.005 — parse-web Lambda silver-tier delivery
to: 2.0.0_SA_COO
cc: 1.0.0_SA_CTO, 0.7.0_AE_CloudOps, 0.1.0_DS_MarketIntelligence~B (sibling score-web feeds my output)

AC1 evidence: parse_web.py at canonical path with from __future__ first import + AST clean + ruff clean
AC2 evidence: deployed to lambda find-insure-parse-web (terraform-apply 0-diff + tag)
AC3 evidence: silver output for 1 smoke IMO at s3://opal-data-imo/corp/{slug}/silver/web-scrape/{date}/ — page count + sample page record + site_index
AC4 evidence: full-100 fan-out — parsed-page count >= bronze-page count * 0.9 (10% loss budget for skipped non-HTML / SPA-empty); site_index per slug
AC5 evidence: 5-page hand-spot-check on the smoke IMO — text + link graph + contact blocks match human read
AC6 evidence: Rule 14/14a/15/17 gates clean (paste outputs)
AC7 evidence: telemetry/ ndjson run record + duration/memory empirical
```

---

## 8. Status of dependencies (snapshot 2026-05-27T16:55Z)

| Dep | State | Owner | My posture |
|---|---|---|---|
| FIND_INSURE.001 (bucket + IAM + secrets) | in_progress per AE TF scaffold pre-apply `3c2d7b3dc` | 0.7.0_AE_CloudOps | Standing; need RAVC2-ACCEPT before AC5 ship |
| FIND_INSURE.003 (comp-graph register) | in_progress per AE | 0.7.0_AE_CloudOps | Non-blocking on my Lambda authoring; required pre-comp-pipescript-deployed-MATCH check |
| FIND_INSURE.004 (crawl-web bronze) | TO not yet authored | ws CTO authoring; AE 0.7 to execute | Defines my INPUT schema; will integrate at TO-drop |
| FIND_INSURE.005 (parse-web, me) | TO not yet authored | ws CTO authoring | I scaffold; integrate at TO-drop |
| FIND_INSURE.006 (score-web, ~B) | TO not yet authored | ws CTO authoring; ~B to execute | Sister-coordinate on silver→gold contract once design briefs converge |
| trafilatura/tldextract Lambda layer | TBD | 0.7.0_AE_CloudOps | Will flag at TO-drop |

---

## 9. Next actions (this session)

1. STANDBY — pull inbox every /work tick for .005 TO drop + AE 0.7 .001 RAVC2 + .004 bronze schema visibility
2. Coordinate with ~B (when spawned) on silver→gold record shape — my output fields (esp. `page_text`, `links_external`, `meta_tags`, `headings`) are score-web inputs per CTO hint #3 (gold consolidates + classifies)
3. On .005 TO drop: integrate any new COO ACs into this brief (v0.3), finalize per-IMO/per-page invocation pattern + runtime pin + trigger mechanism, author `data/find/imo/scripts/silver/web-scrape/parse_web.py`, ship per Rule 13/14/14a/15/17 discipline
4. On parse_web.py ship: smoke single IMO first → RAVC2-stage-1 evidence → full-100 fan-out → RAVC2-Request to ws COO (CC ws CTO + AE 0.7 + ~B)

## 10. Authoring lineage

- **v0.2** 2026-05-27T~17:05Z — ws CTO `[ACK + ARCH-INPUT]` arch-input absorption (CTO MCP 2026-05-27T~17:02Z). 4 hints folded:
   1. BeautifulSoup canonical (DROPPED trafilatura/readability-lxml/tldextract/phonenumbers; lxml as BS backend only)
   2. Per-page schema flat under `{url_hash}.json`; added `content_hash` for change-detection; field naming aligned (`page_text` / `meta_tags` / `links_internal+external` / `contact_blocks.emails+phones`)
   3. Rule-17 preserve-all reinforced — ALL meta tags by name+property (no whitelist); ALL headings h1-h6; ALL link URLs (no host-filter); NO silver-side contact_blocks dedupe; NO silver classification/scoring
   4. Blocked-page minimal-record discipline added — `blocked_reason` enum, audit-trail per PRD §9 Q5
   Open-questions §6 condensed 6→7 (Q2 + Q4 resolved by CTO; Q7 added re: site_index keep-or-drop)
- **v0.1** 2026-05-27T~16:55Z — initial STANDBY-PREP scaffold absorbing PRD v0.3 + CVO arch-brief + allocation #3 brief; trafilatura/readability-lxml/tldextract speculative library shortlist (CTO superseded in v0.2)

— 0.1.0_DS_MarketIntelligence~A 2026-05-27T17:05Z
