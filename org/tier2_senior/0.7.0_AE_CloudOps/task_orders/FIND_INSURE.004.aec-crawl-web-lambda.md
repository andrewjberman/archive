# FIND_INSURE.004 — crawl-web Lambda (per-IMO Bright Data orchestration)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 + §4 Phase 1 deliverable 1
**Pod:** 0.7.0_AE_CloudOps
**Lane:** AE base
**Author:** 2.0.0_SA_COO 2026-05-27T~17:05Z (cycle #171 Phase 1 TO triad dispatch)
**Status:** pending — GO active per Andrew sovereign peak-priority 16:46Z; **self-fire post-.001 RAVC2-Request internal**
**Sizing:** ~3-5h wall (Lambda + Bright Data wiring + fan-out + sample-IMO empirical crawl)

<status>pending</status>

---

## Objective

Author the `crawl-web` Lambda that invokes Bright Data crawler per IMO (recursive within company-domain; depth + page-cap configurable) and writes raw HTML + response metadata to `s3://opal-data-imo/corp/{company-slug}/bronze/web-scrape/{run-date}/`. Per-page file write at `{url_hash}.html` + `{url_hash}.meta.json`.

Lambda is the per-IMO fan-out unit triggered by EventBridge from the `refresh-source-list` extractor (already shipped per FIND_INSURE.002 + .002b). Input event: `{company_slug, website_url, run_date}` per IMO.

## Acceptance criteria

- **AC1.** Lambda code at `data/find/imo/scripts/bronze/crawl_web_bronze.py`. Standard CLAUDE.md discipline (`from __future__ import annotations` first import + ruff py39 clean). Uses Bright Data API per existing `find-insure/bright-data/api-key` Secrets Manager namespace (per .001 AC3 IAM scope).
- **AC2.** Per-page bronze schema: `{page_url, url_hash (sha256 hex truncated to 16 chars), content_hash (sha256 hex truncated to 16 chars of body), fetched_at (ISO-8601-Z), http_status, http_headers, response_body_html, robots_txt_compliance, crawl_depth}`. Separate `.html` + `.meta.json` files per page; the silver Lambda (.005 by ~A) consumes both.
- **AC3.** **`robots.txt` honor-default** per PRD v0.3 §9 Q5: v0.1 default = honor robots.txt; per-IMO override requires Andrew sign-off via Lambda env var override list (do NOT bake permanent allow-list; surface override-class as configurable input).
- **AC4.** Recursive depth-limited crawl within company-domain: max depth = 3 (configurable); max pages = 200 (configurable); domain-bound (do not follow external links). Track URL graph for silver consumption.
- **AC5.** Bare-domain rewrite handling per .002 anomaly list (6 IMOs without `https://`): Carl Ostenson Associates / Developers Marketing Corporation / Gordon Marketing / Highland Capital Brokerage / MiddleOak / Safe Money Resource. http-fallback per-domain tolerance: if `https://` TLS fails, retry `http://` once + flag in metadata (do NOT block crawl on TLS-invalid; preserve universe-completeness).
- **AC6.** Lambda handler signature compatible with EventBridge per-IMO fan-out. Input event: `{company_slug, website_url, run_date}`. Output: page-count crawled + any per-page errors as CloudWatch log.
- **AC7.** Per-IMO bronze-write path: `bronze/web-scrape/{company_slug}/{run-date}/{url_hash}.{html|meta.json}`. Slug from .002b `_util/slugify.py` import.
- **AC8.** Empirical run against ≥3 sample IMOs (mix of large + small + bare-domain class): pages crawled + bronze files committed to S3. Manual spot-check of 1 IMO bronze structure.
- **AC9.** EventBridge wiring: `FIND_INSURE.refresh-source-list` (existing .002 extractor) fan-out trigger to per-IMO `crawl-web` invocations. Concurrency cap = configurable (default 10 parallel per Bright Data rate-limit; AE 0.7 finalizes per Bright Data tier).
- **AC10.** Standard CLAUDE.md deploy: Terraform Lambda module for crawl-web + safe-apply + tag `find-insure-v1.0.x` post-0-diff + record-terraform-deploy. comp-iam service for s3:PutObject + secretsmanager:GetSecretValue (bright-data namespace) + cloudwatch:PutMetricData; comp-pipescript io for code-structure verify.

## Dependencies

- **FIND_INSURE.001 RAVC2-Accept** — bucket must exist for bronze write; `find-insure-lambda-role` must exist for permissions; `find-insure/bright-data/api-key` secret must be confirmed-accessible. **.004 self-fires post-.001 RAVC2-Request** per Andrew sovereign 16:46Z peak-priority + your KEEP-LIVE active session.
- **No upstream code dependency** — refresh-source-list extractor (.002) already shipped + path-relocated; output structure stable. Slugify (.002b) shipped.
- **Downstream:** .005 parse-web (~A) reads your bronze; sister-coord on bronze schema via [SYNC] if breaking change.

## Self-fire trigger (no separate [DRIVE-GO] needed)

Per Andrew sovereign peak-priority + your KEEP-LIVE: on completion of FIND_INSURE.001 RAVC2-Request (your own ship to me), continue immediately to .004 + .003 (comp-graph registration; AE 0.7 lane). No COO acknowledgment overhead. .004 RAVC2-Request lands at me when AC1-AC10 met.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.004 — crawl-web Lambda` to ws COO with: code commit hash + Terraform plan-apply 0-diff confirm + tag commit hash + EventBridge wiring + AC8 empirical crawl output (page-count + S3 ls of one sample IMO's bronze + spot-check meta.json structure) + comp-iam service + comp-pipescript io output. CC ws CTO + DS~A (silver downstream contract).

## Notes

- Per PRD v0.3 §3.3 Bright Data is the canonical crawl tool; do NOT use beautifulsoup or requests directly for crawl-stage (that's silver-tier's parser job per .005).
- Per CLAUDE.md Rule 12 (S3 artifact store) — bronze files live in S3, not on EC2/Lambda local disk.
- Phase 1 sub-2h-per-Lambda target may slip on .004 if Bright Data rate-limits or large-site crawl latency surfaces. Flag via [BLOCKED-ASK] if you hit a wall; ws CTO has authority to adjust depth/page-cap defaults.
- 99-IMO universe per .002 ship — full Phase 1 RAVC2 (≥90% on 100-IMO per PRD AC2) gates on this Lambda running against full universe.

— ws COO /drive #171 Phase 1 TO triad 2026-05-27T17:05Z
