# FIND_INSURE.005 — parse-web Lambda (HTML → silver structure)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 + §4 Phase 1 deliverable 2
**Pod:** 0.1.0_DS_MarketIntelligence~A
**Lane:** DS_MarketIntelligence ~A (Phase 1 silver-tier authoring)
**Author:** 2.0.0_SA_COO 2026-05-27T~17:05Z (cycle #171 Phase 1 TO triad dispatch)
**Status:** pending — GO active per Andrew sovereign peak-priority 16:46Z
**Sizing:** ~3-5h wall (Lambda development + unit tests + sample-IMO empirical run)
**Design baseline:** `752b1fcee` — DS~A design brief v0.2 already absorbed ws CTO 4 hints + ~B silver→gold contract handshake

<status>pending</status>

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
