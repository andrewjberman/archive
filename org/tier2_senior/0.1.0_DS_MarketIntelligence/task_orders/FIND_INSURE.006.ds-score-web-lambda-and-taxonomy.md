# FIND_INSURE.006 — score-web Lambda + indicator-term taxonomy

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 + §4 Phase 1 deliverable 3
**Pod:** 0.1.0_DS_MarketIntelligence~B
**Lane:** DS_MarketIntelligence ~B (Phase 1 gold-tier authoring + taxonomy author)
**Author:** 2.0.0_SA_COO 2026-05-27T~17:05Z (cycle #171 Phase 1 TO triad dispatch)
**Status:** pending — GO active per Andrew sovereign peak-priority 16:46Z
**Sizing:** ~3-5h wall (Lambda + taxonomy v1 + sample-IMO empirical scoring)
**Design baseline:** STANDBY-PREP staged uncommitted (taxonomy v0.1 draft + design brief skeleton per your /work-cycle:1 absorbed)

<status>pending</status>

---

## Objective

Author the `score-web` Lambda that consumes per-IMO silver structured content (from FIND_INSURE.005 parse-web) and emits per-IMO gold scoring against the asset-management-transition indicator-term taxonomy. **Term-class taxonomy IS itself a deliverable** per PRD v0.3 §4 Phase 1 deliverable 3.

Gold output lands at `s3://opal-data-imo/corp/{slug}/gold/web-scrape/{run-date}/`. Shared taxonomy config lands at `s3://opal-data-imo/config/term-taxonomy-v1.json` (first-fire of `config/` prefix per CVO arch-brief §3).

## Acceptance criteria

- **AC1.** Lambda code at `data/find/imo/scripts/gold/score_web_gold.py`. Standard CLAUDE.md DS discipline: `from __future__ import annotations` first import; ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** Taxonomy v1 config at `data/find/imo/config/term-taxonomy-v1.json` containing 15+ seed terms per PRD v0.3 §4 Phase 1 minimum: `RIA, Registered Investment Advisor, asset management, wealth management, Series 65, Series 66, Series 7, Series 24, Series 6, IAR, fiduciary, AUM, investment advisory, Form ADV, model portfolio, SMA, TAMP` + your extensions with class-grouping (regulatory-license-class / business-model-class / product-class / certification-class per your earlier MCP offer).
- **AC3.** Taxonomy JSON schema:
  ```json
  {
    "version": "v1",
    "authored": "2026-05-27",
    "author": "0.1.0_DS_MarketIntelligence~B",
    "terms": [
      {"term": "RIA", "class": "regulatory-license", "weight": 1.0, "match_type": "exact_or_word_boundary"},
      {"term": "Registered Investment Advisor", "class": "regulatory-license", "weight": 1.0, "match_type": "case_insensitive"},
      ...
    ]
  }
  ```
  Match-type taxonomy: `exact_or_word_boundary` / `case_insensitive` / `regex` (with regex field for the latter).
- **AC4.** Per-IMO gold schema: `{company_slug, run_date, term_matches: [{term, class, page_url, context_snippet, position}], term_match_count, term_class_distribution, rollup_score, scored_at}`. Context snippet ~50 chars before/after each match for IR-team-readability.
- **AC5.** Scoring formula v0.1: `rollup_score = sum over terms (term_weight × log(1 + match_count_per_term))` capped at term-class diversity bonus (penalize single-term-spam; reward cross-class signal). Final scores normalized 0-100 for IR-team-readability. Document formula in module docstring.
- **AC6.** Lambda handler signature compatible with EventBridge per-IMO fan-out from .005 parse-web. Input event: `{company_slug, run_date, silver_prefix}`. Reads taxonomy from S3 `config/term-taxonomy-v1.json` at cold-start (cache for warm); reads silver pages for the IMO; emits gold score.
- **AC7.** Empirical run against same ≥3 sample IMOs as .005 (Carl Ostenson / Developers Marketing / Gordon Marketing OR larger IMOs like Advisors Excel / Allianz Life with rich asset-mgmt content). Verify score plausibility via manual spot-check: at least 1 IMO with high score (visible asset-mgmt language) + 1 with low score (insurance-only language).
- **AC8.** Sister silver→gold contract per ~A handshake locked: gold reads silver fields per AC2 of .005; coordinate on any silver-schema breaking change via [SYNC] to ~A.
- **AC9.** Taxonomy hot-swap-safe contract: gold Lambda reads taxonomy version at runtime; v2 doesn't break v1 existing scores (version-pinned in gold output `taxonomy_version` field).
- **AC10.** comp-pipescript io after code lands; comp-iam service (verifies s3:GetObject on `config/*` + s3:PutObject on `corp/*/gold/web-scrape/*` under `find-insure-lambda-role`).

## Dependencies

- **FIND_INSURE.001 RAVC2-Accept** — bucket must exist for config + gold write.
- **FIND_INSURE.005 parse-web** — silver schema is your INPUT contract per ~A handshake. You may author + draft against design brief silver schema; final AC7 empirical run requires .005 silver output exists.
- **No other downstream gate** — Phase 3 (~E serving-build) reads your gold; that's downstream Phase 3 dependency on your output.

## Sequencing — STANDBY-PREP compress-to-delivery

Per your /work-cycle:1 staging (taxonomy v0.1 + design brief skeleton):
1. **NOW (within ~1-2h):** complete taxonomy v1 ratified + commit config/term-taxonomy-v1.json; complete Lambda code; unit tests against synthetic silver fixtures
2. **On .001 RAVC2-Accept:** config file lands at S3; AC2 + AC10 evidence
3. **On .005 silver ship:** AC7 empirical scoring against real silver

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.006 — score-web Lambda + taxonomy v1` to ws COO with: code commit hash + taxonomy JSON commit hash + unit tests + AC7 empirical scoring (≥3 IMOs; spot-check 1 high + 1 low) + comp-pipescript io output + sister-coord confirmation with ~A. CC ws CTO + AE 0.7 + ~E (Phase 3 will consume your gold).

## Notes

- Taxonomy v2 will surface from Phase 1 empirical run + Phase 2 + IR-team feedback. v1 = starting baseline; PRD §4 framing supports extension.
- Per [[feedback_silver_no_field_slimming]] companion — gold IS allowed to apply business-logic + scoring; this is the gold-tier license-class differentiation point per CLAUDE.md Rule 17.
- Score normalization 0-100 chosen for IR-team-readability (Andrew framing); raw rollup also preserved in gold for re-normalization downstream.
- Phase 2 Part A LinkedIn scoring (`score_linkedin_gold.py` by ~C) will sister this pattern. Phase 2 Part B job-postings scoring (`score_jobs_gold.py` by ~D) similarly.

— ws COO /drive #171 Phase 1 TO triad 2026-05-27T17:05Z
