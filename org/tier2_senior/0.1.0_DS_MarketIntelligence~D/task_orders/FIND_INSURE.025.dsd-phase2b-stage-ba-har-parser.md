# FIND_INSURE.025 — Phase 2B Stage Bα HAR parser (job-postings channel) — staged

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4+ §4 Phase 2B Stage Bα (HAR-analysis primary path)
**Pod:** 0.1.0_DS_MarketIntelligence~D
**Lane:** DS_MarketIntelligence ~D (Phase 2B job-postings channel execution)
**Issued to:** 0.1.0_DS_MarketIntelligence~D
**Author:** 2.0.0_SA_COO 2026-05-27T~23:14Z (cycle 165 forward-staging — Phase 2B Stage Bα pre-author per Andrew goal-set 22:49Z FIND_INSURE end-to-end drive)
**Sizing:** ~3-5h wall (per-board HAR parser + bronze emit + silver schema + ~5 unit-tests per board; Andrew HAR captures gate)
**Authority anchor:** Andrew sovereign goal-set 2026-05-27T~22:49Z + Andrew direct 2026-05-15 SXPL_RESTIN-pattern analogue (HAR-analysis primary, Bright Data fallback for HAR-infeasible boards).

<status>staged</status>
<dispatch_held>true</dispatch_held>
<dispatch_unlock_gate>Andrew supplies HAR captures from at least 1 job-posting board (Glassdoor, Indeed, LinkedIn-jobs, or per Andrew's board preference). Each HAR enables 1 per-board parser; per-board TO instances spawn from this template.</dispatch_unlock_gate>

## Objective

Author the HAR-parser Lambda for one or more job-posting boards (Glassdoor + Indeed + LinkedIn-jobs primary candidates) using Andrew-supplied HAR captures per SXPL_RESTIN-pattern. Each per-board parser extracts job-postings JSON from HAR network requests, emits bronze records per medallion convention, then chains to silver/gold for job-posting scoring (investment-keyword + Series-license + corp-finance/tech-hire detection per CVO § FIND_INSURE PRD v0.4 §4 Phase 2B).

**Per-board scope (parallel):** if Andrew supplies HAR from Board X, this TO instance covers Board X. Additional boards spawn additional TO instances (.025b, .025c, etc.).

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import on all bronze/silver/gold scripts; ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** Andrew HAR supply at canonical path: `data/find/imo/config/har/{board}-{capture-date}.har` (e.g., `glassdoor-2026-05-28.har`). HAR file is gitignored OR sanitized (no PII) — coordinate with ws CTO on Andrew-supply-path convention.
- **AC3.** HAR-parser script at `data/find/imo/scripts/_util/har_parser_{board}.py` — reads HAR file + extracts target API requests (job-posting search results endpoint per Andrew's analysis) + emits structured job-posting records.
- **AC4.** Bronze emit: `corp/{slug}/bronze/job-postings/{board}/{run-date}/{job_id}.json` per medallion convention. ONE record per job-posting (not per HAR file).
- **AC5.** Silver Lambda at `data/find/imo/scripts/silver/parse_jobs_silver.py` — bronze → silver schema (Rule 17 strict). Schema: `{job_id, posted_at, title, company_slug, board_source, location, description, job_keywords[], series_license_mentions[], corp_finance_or_tech_hire_class, raw_metadata}` (per CVO Phase 2B scoring framework).
- **AC6.** Gold Lambda at `data/find/imo/scripts/gold/score_jobs_gold.py` — silver → gold scoring. Per-job rollup_score based on:
  - `investment_keyword` weight (per scoring-weights-v0.1.json job-postings sub-config) — investment-mgmt, asset-mgmt, portfolio, wealth-mgmt mentions
  - `series_license` weight — Series 7/24/63/65/66/79 explicit license requirements
  - `corp_finance_or_tech_hire_class` weight — corporate finance OR tech hires (signals scaling)
  - `recency` damping — newer postings weighted higher (per CVO ADDITIVE-1 hiring-signal class)
- **AC7.** Per-IMO aggregate: `corp/{slug}/gold/job-postings/{run-date}/aggregate.json` with `{job_postings_count, total_score, top_job_signals[], aggregated_hiring_signal_class}` — feeds Phase 3 `serving/scoring.json` `hiring_signal_class` field per CVO ADDITIVE-1.
- **AC8.** Lambda dispatch pattern: standalone (HAR is one-shot per Andrew-supplied capture, not EventBridge-fired) — local invocation via `python har_parser_{board}.py --input data/find/imo/config/har/{board}-{capture-date}.har --output-prefix corp/`.
- **AC9.** HAR validation: parser MUST gracefully degrade on malformed HAR (warn + skip + emit `parse_errors_{board}.json` log) — Andrew HAR captures may not be canonical Chrome DevTools exports; defensive parsing required.
- **AC10.** Cost: $0 LushaAI cost (HAR-based, no API calls); standalone Lambda execution + S3 PutObject only.
- **AC11.** `comp-pipescript io` clean (after AE comp-graph registration); `comp-iam service` confirms s3:PutObject scope.

## Dependencies

- **Andrew HAR supply** — HARD GATE per Andrew direct 2026-05-15 SXPL_RESTIN-pattern; until Andrew supplies at least 1 board's HAR captures, this TO stays staged.
- **PRD §4 Phase 2B scope ratify** — PRD v0.4+ documents Phase 2B Stage Bα as HAR-staged-primary; refine per Andrew Q1 ratify timing.
- **AE 0.7 Lambda deploy substrate** — Phase 2B silver + gold Lambdas need deployment via find-insure Terraform module; HAR parser may run as standalone Python (not Lambda) initially given one-shot nature.
- **FIND_INSURE.016 (DS~D job-board public-API survey)** — RECOMMENDED predecessor: surveys which boards have public APIs vs require HAR. Informs whether Stage Bα HAR-only is sufficient OR Stage Bβ Bright Data fallback needed.

## Sequencing — staged pending Andrew HAR

**Pre-gate (NOW; pre-stage design):**
1. ~30min: read `.016` survey output (when shipped) + SXPL_RESTIN HAR-analysis pattern doc (`docs/briefs/sxpl-restin-har-staged-plan.md` if exists OR ask ws COO)
2. ~1h: author design brief at `.../deliverables/phase2b_har_parser_design_v0.1.md` — per-board parser pattern + bronze schema + silver passthrough rules + gold scoring formula

**Post-gate (Andrew supplies HAR; GO fires):**
3. ~30min: HAR sanity-check + extract sample job-postings + validate schema mapping
4. ~2h: HAR parser + silver Lambda + gold Lambda + unit tests per board
5. ~30min: empirical run against Andrew HAR + spot-check
6. ~15min: commit + RAVC2-Request

**Total ETA:** ~3-4h wall post-Andrew-HAR per board; ~1-2h pre-gate design authoring.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.025 — Phase 2B Stage Bα HAR parser ({board})` to ws COO. CC ws CTO + ws CVO. Body: code commit hash + per-board HAR parse evidence (sample job-posting count + extracted job_keywords sample + corp_finance_or_tech_hire classification spot-check) + cost-gate compliance ($0 expected) + comp-pipescript/comp-iam outputs.

## Sister coord

- **FIND_INSURE.016 (your prior staged TO, job-board public-API survey)** — informs HAR-vs-API choice per board; survey results may indicate some boards have public APIs (use those instead of HAR for those boards)
- **FIND_INSURE.024 (Phase 2A LushaAI LIVE-DISPATCH; DS~C)** — Phase 2A subset is INDEPENDENT of Phase 2B job-postings universe; both feed Phase 3 separately. No content overlap.
- **Stage Bβ Bright Data fallback** — if Andrew HAR supply is partial (e.g., Glassdoor HAR available but Indeed HAR not feasible), Bright Data fallback Lambda spawns separately as Stage Bβ TO (likely .025-fallback or .026).

## Notes

- Per Andrew direct 2026-05-15 SXPL_RESTIN-pattern: HAR-staged-primary is the v0.1 path; Bright Data fallback is deferred.
- Per [[feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch]]: pre-stage design + parser-pattern + scoring-formula NOW so Andrew-HAR-supply-moment to ship is ~3h wall.
- CVO ADDITIVE-1 `hiring_signal_class` field per .023 schema integration — your AC7 aggregate output feeds it.
- Andrew HAR is one-shot per board per capture session — if board layouts change, fresh HAR captures required (operational discipline note).

— ws COO /drive cycle 165 forward-staging — Phase 2B Stage Bα HAR parser pre-author 2026-05-27T~23:14Z
