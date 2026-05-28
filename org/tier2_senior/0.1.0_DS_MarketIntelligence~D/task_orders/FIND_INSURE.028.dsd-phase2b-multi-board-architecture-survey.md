# FIND_INSURE.028 — Phase 2B multi-board architecture survey + per-board parser system design (DS~D)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4+ §4 Phase 2B + Stage Bα/Bβ routing per Andrew direct 2026-05-15 SXPL_RESTIN-pattern
**Pod:** 0.1.0_DS_MarketIntelligence~D
**Lane:** DS_MarketIntelligence ~D (Phase 2B job-postings channel architecture + exploration)
**Issued to:** 0.1.0_DS_MarketIntelligence~D
**Author:** 2.0.0_SA_COO 2026-05-27T~23:28Z (cycle 165 Andrew 23:25Z parallelize-directive exploration TO)
**Sizing:** ~4-6h wall (multi-board survey + parser system design + Stage routing matrix + structured documentation)
**Authority anchor:** Andrew direct 2026-05-27T~23:25Z verbatim: "various channel architecture using various job boards (exploring them and developing systems)" + 2026-05-27T~23:26Z verbatim: "have them document their findings in structured format" + Andrew goal-set 22:49Z FIND_INSURE end-to-end drive.

<status>complete</status>
<!-- RAVC2-ACCEPT-CLOSE by ws COO 2026-05-28T~00:08Z (all 10 ACs PASS; Tier-3 Wave-1 promotion RATIFIED; AC10 HAR-ask enumeration FORWARDED TO ANDREW). Deliverables: AC1 docs/reference/job-board-channel-architecture-matrix.md + AC2 docs/briefs/find-insure-phase2b-multi-board-design-v0.1.md + AC3 docs/reference/find-insure-phase2b-stage-routing-matrix.md + AC4 docs/briefs/find-insure-phase2b-cross-board-analytics-v0.1.md + AC5 data/find/imo/scripts/_util/har_parser_base.py. Commits fbe1bf264 (4-artifact suite + AC5) + 2f2ec094d (AC4 v0.1.1 CVO SUBSTANCE-META YELLOW->GREEN fix). Path-flag (docs/briefs vs docs/architecture for AC2/AC4) ACCEPTED by ws COO. Status tag corrected here 2026-05-28 (was lagging at pending). -->
<dispatch_held>false</dispatch_held>

## Objective

Survey ALL candidate job-posting boards relevant to FIND_INSURE Phase 2B (asset-management transition detection via hiring signals) + author per-board parser system design pattern + Stage Bα/Bβ routing decision matrix + cross-board correlation analytics framework. **Deliverables are structured documentation artifacts** per Andrew 23:26Z directive + a per-board parser scaffolding pattern (one canonical implementation + N-board instantiation discipline). This is exploration + system design — NOT yet HAR parsing execution (that's `.025` once Andrew supplies HARs).

## Candidate boards (initial survey scope)

- **Tier 1 (PRD-cited):** Glassdoor + Indeed + LinkedIn-jobs
- **Tier 2 (likely-additive):** ZipRecruiter + Monster + CareerBuilder + Wellfound (formerly AngelList Talent)
- **Tier 3 (industry-specific):** eFinancialCareers + InsuranceJobs.com + WealthManagementJobs.com
- **Andrew-additional (per-Andrew direct supply):** any board Andrew explicitly mentions; this TO accommodates additions

## Acceptance criteria

- **AC1.** **Structured artifact 1: `docs/reference/job-board-channel-architecture-matrix.md`** — per-board section covering:
  - Board name + URL + parent company (e.g., Glassdoor owned by Indeed/Recruit Holdings)
  - Search-query UI accessibility (public search vs login-walled)
  - Job-posting page schema (key fields surface-able: title, company, location, posted_date, description, salary_range, qualifications, etc.)
  - API availability (public REST API vs scraping-only vs HAR-only)
  - HAR-feasibility classification (Stage Bα candidate: open-search-page-with-HAR-extractable-JSON) vs Stage Bβ (requires Bright Data scraping)
  - Anti-bot mechanism class (None / Cloudflare / DataDome / proprietary)
  - Rate-limit + ToS-class (any board flag for proxy-rotation requirement)
  - **Decision-relevance class for FIND_INSURE:** which job-posting types signal asset-management transition (e.g., "Portfolio Manager" + "RIA" + "Series 65/66 required" + "CFA preferred")
- **AC2.** **Structured artifact 2: `docs/architecture/find-insure-phase2b-multi-board-design.md`** — per-board parser system design pattern:
  - Canonical HAR parser shape (single `_util/har_parser_base.py` class with per-board specialization via subclass — pattern per SXPL_RESTIN-analogue)
  - Per-board parser module pattern: `_util/har_parser_{board}.py` extends base + implements `extract_job_postings(har_dict) -> List[JobPostingRecord]`
  - Bronze record schema (cross-board universal) + per-board metadata extension
  - Silver record schema (Rule 17 strict passthrough per CLAUDE.md)
  - Gold record scoring pattern (cross-board score normalization for fair ranking)
  - Cross-board deduplication (same job posted to Glassdoor + Indeed + LinkedIn-jobs — dedupe by `(title, company, posted_date, location)` composite key)
  - Per-board parser test-fixture pattern (synthetic HAR + sample-job-posting fixture)
- **AC3.** **Structured artifact 3: `docs/reference/find-insure-phase2b-stage-routing-matrix.md`** — Stage Bα vs Stage Bβ routing decision matrix:
  - Per-board classification: Stage Bα (HAR-feasible; Andrew supplies HAR) vs Stage Bβ (Bright Data scraping_browser1; AE 0.7~B Lambda deploy)
  - Cost-implication per stage class (HAR = $0 + manual capture; Bright Data = per-page ~$0.X)
  - Per-board ToS-class disposition (which boards explicitly prohibit scraping; which require partner-API)
  - Fallback discipline: if Stage Bα HAR captures partial (e.g., Andrew supplies Glassdoor HAR but Indeed HAR infeasible) → Indeed routes to Stage Bβ
  - Update-frequency recommendations (Andrew HAR captures refresh cadence; Bright Data Lambda cron cadence)
- **AC4.** **Structured artifact 4: `docs/architecture/find-insure-phase2b-cross-board-analytics.md`** — cross-board correlation analytics framework:
  - Cross-board signal aggregation (one company posting same role on 3+ boards = high-conviction hiring signal)
  - Hiring-pace metrics (count of new postings per IMO per month — accelerating = growth-class signal per CVO ADDITIVE-1)
  - Investment-keyword density per IMO (cross-board aggregate)
  - Series-license requirement frequency (cross-board)
  - Corp-finance / tech-hire class detection (Andrew's "begets m&a/growth activity" framing per PRD)
  - Phase 3 serving table integration: `serving/hiring_signals.json` cross-IMO ranked table
- **AC5.** **Optional artifact 5 (pre-stage scaffolding): `data/find/imo/scripts/_util/har_parser_base.py`** — canonical base class implementation (no per-board parsers yet — those land in .025 + per-board sub-TOs)
- **AC6.** All 4 (or 5 with AC5) artifacts conform to canonical doc-of-record discipline: title + author + date + authority-chain header + per-section markdown structure + cross-references
- **AC7.** No live HAR parsing execution (gated on Andrew HAR supply per .025); no live Bright Data Lambda dispatch (gated on AE 0.7~B Lambda deploy); cost = $0
- **AC8.** Sister-coord with FIND_INSURE.016 (your prior staged TO, job-board public-API survey) — your AC1 board-classification informs which boards have public APIs (use those instead of HAR/Bright Data for those boards); fold .016 findings into AC1
- **AC9.** Cross-reference: AC4 cross-board analytics feeds into FIND_INSURE.023 (DS~E serving consolidation) `serving/scoring.json` `hiring_signal_class` field per CVO ADDITIVE-1
- **AC10.** **HAR-request enumeration:** AC1 per-board section explicitly tags which boards need Andrew HAR supply (per Andrew 23:27Z "if you need any HARs now is the time to ask" — your AC1 enumerates the ask precisely; ws COO surfaces to Andrew based on your enumeration)

## Dependencies

- **PRD `docs/architecture/FIND_INSURE.md` v0.4+** — §4 Phase 2B + Stage Bα/Bβ routing
- **SXPL_RESTIN-pattern reference** — Andrew direct 2026-05-15 SXPL_RESTIN HAR-analysis-primary precedent (docs/briefs/sxpl-restin-har-staged-plan.md if exists OR ask ws COO for canonical reference)
- **`docs/reference/lusha-api-v3.md`** — sister reference for the LinkedIn-channel (NOT Phase 2B scope; for cross-reference only)
- **FIND_INSURE.016 (your prior staged TO)** — job-board public-API survey — informs AC1 board-classification
- **FIND_INSURE.025 (your other staged TO)** — Stage Bα HAR parser execution — your AC2 design informs .025 implementation pattern

## Sequencing — survey + design phase

1. ~1h: read PRD §4 Phase 2B + SXPL_RESTIN-pattern + Andrew Lusha API v3 ref (cross-reference) + your prior .016 + .025 staged TOs
2. ~1.5h: AC1 — author `job-board-channel-architecture-matrix.md` (per-board deep-dive; ~10-15 boards)
3. ~1.5h: AC2 — author `find-insure-phase2b-multi-board-design.md` (parser system pattern + cross-board dedupe)
4. ~1h: AC3 — author `find-insure-phase2b-stage-routing-matrix.md` (Stage Bα/Bβ routing + ToS-class)
5. ~30min: AC4 — author `find-insure-phase2b-cross-board-analytics.md` (correlation analytics framework)
6. ~30min: AC5 (optional pre-stage scaffolding) — `har_parser_base.py` canonical base class
7. ~30min: AC8 sister-coord with FIND_INSURE.016 + AC9 sister-coord with DS~E .023 + AC10 HAR-request enumeration
8. ~15min: commit + RAVC2-Request

**Total ETA:** ~6h wall from spawn-LIVE (or ~5.5h without AC5 scaffolding).

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.028 — Phase 2B multi-board architecture survey + 4-artifact documentation + per-board HAR ask enumeration` to ws COO. CC ws CTO + ws CVO + DS~E (sister-coord for .023 analytics integration). Body: commit hash + per-artifact summary + per-board classification table (Stage Bα/Bβ) + decision recommendations + AC10 explicit HAR-ask enumeration (which boards need Andrew HAR; which can use Stage Bβ Bright Data fallback).

## Compiler tools mandate

- AC5 if shipped: `.tools/ds-commit-gate.sh data/find/imo/scripts/_util/har_parser_base.py` PASS
- N/A otherwise (exploration + documentation)

## Cross-domain coordination

- **FIND_INSURE.016** — fold findings into AC1; sister-coord on board-API vs HAR-vs-Bright-Data classification
- **FIND_INSURE.025** — your AC2 + AC3 design informs the .025 per-board HAR parser implementation pattern; .025 absorbs your design
- **FIND_INSURE.023 (DS~E serving consolidation)** — AC4 cross-board analytics feeds `serving/scoring.json` `hiring_signal_class` field
- **AE 0.7~B (new spawn per /allocation 23:27Z URGENT)** — your AC3 Stage Bβ routing matrix informs AE 0.7~B's Bright Data fallback Lambda deploy scope

## Notes

- Per Andrew 23:25Z parallelize directive — this TO is concurrent with .025 (HAR parser execution) + .016 (board API survey) + others. Your DS~D lane carries the Phase 2B architecture-design role.
- Per Andrew 23:26Z structured-format directive — every finding lands as a doc-of-record artifact, not inline-only commentary.
- Per Andrew 23:27Z HAR ask opening — your AC10 explicit enumeration is the precise list ws COO surfaces to Andrew. Anticipate: Andrew will supply HARs for boards you mark Stage Bα + high-priority; remaining boards route to Stage Bβ Bright Data per AE 0.7~B.
- Per [[feedback_silver_no_field_slimming]] / Rule 17 — your AC2 silver schema must explicitly respect HAR-extracted-job-posting passthrough; gold filters by investment-keyword + Series-license; do NOT prune at silver.
- Per CVO ADDITIVE-1 hiring-signal-class integration — your AC4 cross-board analytics is the substrate for the `serving/scoring.json` `hiring_signal_class` field per .023.
- Tier 3 boards (eFinancialCareers + InsuranceJobs.com + WealthManagementJobs.com) are particularly high-leverage for FIND_INSURE because they're industry-specific — investment-mgmt or insurance scope — which directly tunes the signal-to-noise ratio versus generalist boards.

— ws COO 2.0.0_SA_COO 2026-05-27T~23:28Z — Phase 2B multi-board architecture survey per Andrew 23:25Z parallelize + 23:26Z structured-format + 23:27Z HAR-opening directives
