# FIND_INSURE.016 — Phase 2B job-board public-API survey (DS~D)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.5 §4 Phase 2B + §9 Q6 (Andrew HARs gate)
**Brief:** `docs/briefs/find-insure-phase2b-public-api-survey-prep-20260527.md` (`e3fcefba9` ws CTO)
**Pod:** 0.1.0_DS_MarketIntelligence~D
**Lane:** DS_MarketIntelligence ~D (Phase 2B per-board survey-prep — Andrew HARs prioritization input)
**Author:** 2.0.0_SA_COO 2026-05-27T~20:02Z (cycle #186 pace-pickup per Andrew sovereign 19:50Z)
**Status:** active — GO-fired via [GO FIND_INSURE.016] MCP `20260527T193133Z`
**Sizing:** ~3-5h wall (6-board survey + comparative table + executive summary)

<status>active</status>

---

## Objective

Survey 6 publicly-documented job-board APIs + comparative schema table + public-doc gap analysis. Output = **Andrew Q6 HARs prioritization brief**: which boards Andrew should target first for HARs collection to unblock Phase 2B per-board Lambda implementation.

Phase 2B per-board Lambda implementation cannot start without Andrew HARs delivery; Andrew HARs prioritization needs your survey to target high-confidence boards first.

## Boards in scope

1. **Glassdoor** (jobs + reviews)
2. **Indeed** (jobs feed + employer-detail)
3. **LinkedIn Jobs** (separate from LinkedIn Sales Nav — distinct API surface)
4. **ZipRecruiter** (jobs feed)
5. **Monster** (jobs feed)
6. **SimplyHired** (jobs feed)

## Acceptance criteria

- **AC1.** Per-board summary table: endpoint base URL + auth model (API key / OAuth / scraping-required) + rate-limit doc + pricing tier + GDPR/CCPA disclosure. Source from public docs only.
- **AC2.** Per-board response-shape summary (JSON Schema or representative-sample) for jobs-list + job-detail endpoints. Extract from public docs; cite docs URLs.
- **AC3.** Per-board public-doc gap analysis — "what would Andrew HARs reveal that public docs don't?" (anti-bot heuristics, undocumented endpoints, request-header signature dependencies, cookie/session flows, etc.).
- **AC4.** Phase 2B PRD §9 Q6 pre-HAR feasibility per-board estimate: **HIGH-confidence-public-API** / **MEDIUM-confidence-needs-HARs** / **LOW-confidence-scraping-only**. Informs Andrew's HARs prioritization ranking.
- **AC5.** Comparative cross-board table summarizing AC1-AC4 + executive summary paragraph (~250 words) on Phase 2B per-board ship-priority ranking.

## Deliverable structure

Single deliverable: `docs/briefs/find-insure-phase2b-job-board-public-api-survey-v0.X.md`

Optional alongside: `data/find/imo/tests/fixtures/phase2b/` response-shape fixtures per board if you scaffold representative samples for downstream Lambda authoring (Phase 2B per-board Lambda devs consume these as design input).

## Sister-coord with DS~C

DS~C `.011 lusha_client.py` shared utility = pattern template for Phase 2B per-board clients (rate-limit handling primitive + error-class taxonomy + mock/fixture testing). MCP DS~C directly if pattern questions surface.

## Phase 2B downstream-gate context

Your survey output unblocks:
- Andrew Q6 HARs prioritization (Andrew decides which boards to target first based on your survey)
- Phase 2B per-board Lambda implementation start (AE~B has scaffold `33d6bcc1f` ready as mechanical-fill substrate)
- HAR-to-manifest cycle compresses ~30-60min vs ~3-6h wall per CTO brief

## Lane discipline

- `docs/briefs/find-insure-phase2b-*.md` — your DS-lane scope (briefs authoring permitted under POD1)
- `data/find/imo/tests/fixtures/phase2b/**` (if you scaffold) — POD1 fixture authoring

## RAVC2 trigger

RAVC2-Request fires when all 5 ACs self-attested PASS. Bundled single-deliverable per CTO+COO ratification (no per-board parallelization).

## Self-classification per /work LD-0072

If blockers surface (e.g., public docs gated behind paywall, anti-scraping ToS questions, GDPR/CCPA ambiguity): `[BLOCKED-ASK]` to COO per LD-0116.

CC: 1.0.0_SA_CTO (brief author + design authority) + 0.1.0_DS_MarketIntelligence~C (sister-coord on shared client-utility pattern) + 0.7.0_AE_CloudOps~B (downstream Phase 2B Lambda implementer; scaffold `33d6bcc1f` consumes your survey output) + 0.1.0_DS_MarketIntelligence base (parent lane visibility)
