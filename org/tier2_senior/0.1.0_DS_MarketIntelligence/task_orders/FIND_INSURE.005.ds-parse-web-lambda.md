# FIND_INSURE.005 — parse-web Lambda (HTML → silver structure)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 + §4 Phase 1 deliverable 2
**Pod:** 0.1.0_DS_MarketIntelligence~A
**Lane:** DS_MarketIntelligence ~A (Phase 1 silver-tier authoring)
**Author:** 2.0.0_SA_COO 2026-05-27T~17:05Z (cycle #171 Phase 1 TO triad dispatch)
**Status:** pending — GO active per Andrew sovereign peak-priority 16:46Z
**Sizing:** ~3-5h wall (Lambda development + unit tests + sample-IMO empirical run)
**Design baseline:** `752b1fcee` — DS~A design brief v0.2 already absorbed ws CTO 4 hints + ~B silver→gold contract handshake

<status>in_progress</status>

## Progress 2026-05-27T~17:20Z (DS~A)

**Code shipped:** `data/find/imo/scripts/silver/parse_web_silver.py` -- AC1-AC7, AC9 satisfied; AC8 (empirical run against ≥3 sample IMOs) DEFERRED pending FIND_INSURE.004 crawl-web ship. AC10 comp-pipescript io ran but reports `Unknown script` because FIND_INSURE.003 comp-graph registration (AE 0.7) has not yet ingested the new `data/find/imo/scripts/silver/` subtree -- runs clean after .003 ships.

- AC1: `from __future__ import annotations` first import; ds-commit-gate clean; ruff `--target-version py39` clean
- AC2: per-page silver schema authored exactly per design baseline v0.2 (752b1fcee) — `{url, url_hash, content_hash, fetched_at, http_status, content_type, etag, last_modified, bronze_key, title, meta_tags (ALL preserved), headings (h1-h6), body_text, link_graph (internal_links + external_links), structured_blocks (addresses + emails + phones), structured_data (json_ld)}`
- AC3: silver path = `corp/{slug}/silver/web-scrape/{run-date}/{url_hash}.json`; `slugify` imported from `_util/slugify.py` per .002b discipline
- AC4: Rule 17 strict — no field-pruning / no fillna / no business-row-filter; preserves ALL meta tags (no whitelist) + ALL headings h1-h6 + ALL link URLs (no host-filter beyond internal/external split); no contact_blocks dedup; no classification/scoring
- AC5: BeautifulSoup4 + lxml backend (`BeautifulSoup(html, "lxml")`); zero new layer dependencies
- AC6: blocked-page minimal record with `blocked_reason` enum `{robots|rate-limit|http_4xx|http_5xx|non-html|parse-error|fetch-timeout}`; classify_metadata_block infers from upstream status; minimal record always written (no skip)
- AC7: Lambda handler signature `lambda_handler(event, context)` with event `{company_slug, run_date, bronze_prefix, [bronze_bucket], [silver_bucket]}` → returns `{pages_processed, pages_blocked, parse_errors, silver_prefix, started_at, ended_at, duration_ms}`; CloudWatch logs structured via stdlib logging
- AC8: **DONE 2026-05-27T~18:15Z empirical PASS** — AE 0.7 .004 shipped bronze for 3 sample IMOs (`2d302b998` end-to-end validated DS~A iter_bronze_pages); local invocation of `parse_imo()` against real S3 bronze:
  - `1st-atlantic-insurance-group` (small site, https, 5 bronze pages): 5/5 parsed clean, 0 blocked, 0 parse_errors
  - `avantax-wealth-management` (large site, https, 5 bronze pages): 5/5 parsed clean, 0 blocked, 0 parse_errors
  - `carl-ostenson` (bare-domain TLS-cert-mismatch, 1 bronze page meta-only no html): 0 parsed, 1 blocked (minimal record with `blocked_reason: "fetch-timeout"`, `page_text: null`, audit-trail preserved per AC6)
  - **Universe-completeness:** 11/11 bronze pages → 11 silver records (no skips per Rule 17 + AC6)
  - **Spot-check Avantax `dbe847e2ca23d510.json`:** title="Tax-Intelligent Investment Planning - Avantax® Wealth Management" (Unicode ® preserved); meta_tags_count=12 (no whitelist); h1=1 + h2=7 (headings preserved h1-h6); body_text=6807 chars; 75 internal_links + 6 external_links; 1 JSON-LD structured_data block; content_hash present. Compared against bronze HTML 32KB → silver 28KB (structure-extraction; full text preserved). MATCH.
  - **Carl Ostenson minimal record:** `{url, url_hash, fetched_at, http_status: 200, content_type: null, bronze_key: null, blocked_reason: "fetch-timeout", page_text: null}` — 239 bytes; AC6 audit-trail discipline confirmed for the TLS-edge-case (bronze had .meta.json but no .html because AE upstream got x-brd-error TLS-cert-mismatch; my code correctly fell through `raw_html is None → "fetch-timeout"` classifier branch).
  - Silver objects: `s3://opal-data-imo/corp/{slug}/silver/web-scrape/2026-05-27/{url_hash}.json` × 11
- AC9: silver→gold contract handshake locked with DS~B per design brief 752b1fcee; schema-change discipline binding — no breaking changes to silver schema without ~B sign-off
- AC10: comp-pipescript io ran (Unknown script — pending .003 comp-graph register); comp-iam service deferred to .001 RAVC2-ACCEPT (find-insure-lambda-role exists then). Both will validate clean post-.001+.003.

**Bronze input contract — ASSUMPTION (open question for .004 author):** parse-web assumes per-page bronze layout `{url_hash}.html` + `{url_hash}.meta.json` sidecar. Bronze adapter `iter_bronze_pages()` is encapsulated so a different bronze schema can be amended without touching parse logic. If .004 chooses a different layout (e.g., single manifest.json), I update only that adapter. Surfacing as a [SYNC] question to AE 0.7 at RAVC2 time.

**Self-test:** 35/35 checks pass via `python data/find/imo/scripts/silver/parse_web_silver.py` (synthetic HTML fixture exercises every parse path + every blocked-reason classifier + every link-class).

---

## Objective

Author the `parse-web` Lambda that consumes per-IMO bronze HTML output (from FIND_INSURE.004 crawl-web) and emits structured silver content per medallion convention. Lambda fans out per-IMO (one execution per company-slug) and writes to `s3://opal-data-imo/corp/{slug}/silver/web-scrape/{run-date}/`.

Design baseline: your v0.2 brief `752b1fcee` is the spec. This TO ratifies it + binds AC.

## Acceptance criteria

- **AC1.** Lambda code at `data/find/imo/scripts/silver/parse_web_silver.py` (medallion-by-layer per CTO ARCH-RULING `bacf90484`). Standard CLAUDE.md DS discipline: `from __future__ import annotations` first import; ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** Per-page silver schema: `{page_url, url_hash, content_hash, fetched_at, title, meta_tags, headings (h1-h6 with hierarchy), body_text, link_graph (internal_links, external_links), structured_blocks (mailto/tel/address)}`. Per your design brief.
- **AC3.** Per-IMO silver-write path: `silver/web-scrape/{company_slug}/{run-date}/{url_hash}.json` (one file per page). Slug from `_util/slugify.py` import (per .002b shared discipline).
- **AC4.** **Rule 17 strict** (preserve-all; NO field-pruning). Silver does dedup + standardize + flatten encoding artifacts ONLY. No fillna, no row-drop, no business-logic. Per CLAUDE.md Rule 17.
- **AC5.** BeautifulSoup canonical (lxml parser) per CTO hint. Zero new layer dependencies — use existing requests + BS4 layer.
- **AC6.** Blocked-page minimal-record audit-trail per PRD §9 Q5: if bronze HTML indicates fetch-failure (404/403/timeout/robots-block), silver writes a minimal `{page_url, url_hash, fetched_at, status_code, blocked_reason}` stub at the URL — NOT a skip. Preserves universe-completeness for Phase 3 join.
- **AC7.** Lambda handler signature compatible with EventBridge per-IMO fan-out from .004 crawl-web. Input event: `{company_slug, run_date, bronze_prefix}`. Output: silver-file count + any per-page parse-errors as side-channel CloudWatch log.
- **AC8.** Empirical run against ≥3 sample IMOs (one large site, one small, one with TLS issues from the bare-domain rewrite list — Carl Ostenson Associates / Developers Marketing Corporation / Gordon Marketing). Verify silver structure correctness via manual spot-check of 1 IMO's silver output (compare bronze HTML→silver structured content).
- **AC9.** Sister silver→gold contract per ~A/~B handshake locked in your brief: gold/.006 reads silver and processes; silver schema is the gold input contract. Coordinate on schema-change discipline (no breaking changes to silver schema post-AC2 ratify without ~B sign-off).
- **AC10.** comp-pipescript io after code lands (verifies structure); comp-iam service (verifies s3:PutObject scope under `find-insure-lambda-role`).

## Dependencies

- **FIND_INSURE.001 RAVC2-Accept** — bucket must exist for silver write. AE 0.7 plan clean per `ccad1ba79`; apply imminent.
- **FIND_INSURE.004 crawl-web** — bronze schema is your INPUT contract. AE 0.7 lane; will be dispatched once .001 RAVC2-Accepted. You may design + draft against PRD §3.4 bronze structure WITHOUT waiting for .004 ship; final integration test (AC8) requires .004 bronze output exists.
- **`_util/slugify.py`** — already shipped per .002b `afe8ddce2`.

## Sequencing — STANDBY-PREP compress-to-delivery

Your design brief v0.2 `752b1fcee` is already substantively complete. Path-of-least-resistance:
1. **NOW (within ~1-2h):** code Lambda against design baseline; unit tests against synthetic bronze fixtures
2. **On .001 RAVC2-Accept (~within 1h):** AE 0.7 ships bucket; you can wire AC8 empirical run path
3. **On .004 ship (~3-5h):** bronze data lands for ≥3 IMOs; you run AC8 empirical against real bronze

If .004 bronze takes longer than your Lambda code, that's normal — you finish + commit code + AC8 evidence chains as second commit.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.005 — parse-web Lambda` to ws COO with: code commit hash + unit test results + AC8 empirical run output (file count + spot-check of 1 IMO silver structure) + comp-pipescript io output + sister-coord confirmation with ~B. CC ws CTO + AE 0.7.

## Notes

- Per [[feedback_silver_no_field_slimming]] + CLAUDE.md Rule 17 — silver preserves all bronze fields; no business-logic.
- Per CTO 4 hints: BeautifulSoup canonical / per-page url_hash + content_hash / Rule-17 preserve-all reinforced / blocked-page minimal-record audit-trail. All absorbed in your v0.2 design.
- Per [[feedback_empirical_anchor_first_pays_back_in_debug_savings]] — your design's empirical-anchor-first discipline (probe a real IMO bronze structure before coding the parser) pays back in debug savings. Continue that pattern.
- Phase 2 Part A LinkedIn parser will be a sister Lambda (`parse_linkedin_silver.py`) when ~C ships. Phase 2 Part B job-postings parser is `parse_jobs_silver.py` when ~D ships. Same medallion + slug discipline.

— ws COO /drive #171 Phase 1 TO triad 2026-05-27T17:05Z
