# FIND_INSURE.024 — Phase 2A LIVE-DISPATCH LushaAI enrichment (top-quintile subset) — staged

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4+ §4 Phase 2A (top-quintile + Series-license-mention subset; LushaAI enrichment)
**Pod:** 0.1.0_DS_MarketIntelligence~C
**Lane:** DS_MarketIntelligence ~C (Phase 2A LinkedIn-pipeline live-execution tier)
**Issued to:** 0.1.0_DS_MarketIntelligence~C
**Author:** 2.0.0_SA_COO 2026-05-27T~23:14Z (cycle 165 forward-staging — Phase 2A LIVE-DISPATCH pre-author per Andrew goal-set 22:49Z FIND_INSURE end-to-end drive)
**Sizing:** ~3-5h wall (LushaAI Lambda live-dispatch + per-employee scoring + RAVC2; cost-gate constrained)
**Authority anchor:** Andrew sovereign goal-set 2026-05-27T~22:49Z + CVO Phase 2A entry gates per CVO Mode B comprehensive verify-channel in flight; gates on `.011` RAVC2-Accept + Andrew Q1 subset-cut decision.

<status>staged</status>
<dispatch_held>true</dispatch_held>
<dispatch_unlock_gate>FIND_INSURE.011 RAVC2-Accept (Phase 2A Lambda skeleton + Lusha client + opt-out webhook scaffold all shipped) AND Andrew Q1 sovereign ratify (subset-cut rule: top-quintile + Series-license-mention OR refined criterion)</dispatch_unlock_gate>

## Objective

Execute Phase 2A LushaAI enrichment on the Andrew-Q1-ratified subset of Phase 1 ranked companies. For each company in the subset, invoke the LushaAI integration (Lusha API v3 Search + Prospecting + Enrich endpoints per `docs/reference/lusha-api-v3.md`) to enrich with decision-relevant employees + Series-license counts + AUM extraction. Output: per-IMO LinkedIn-channel bronze/silver/gold + serving-layer employee table.

**Subset boundary:** the Andrew Q1 rule applied to Phase 1 `serving/scoring.json` ranked output produces the Phase 2A subset. Recommended provisional rule (refines per Andrew ratify):
- Tier 1: top quintile by `rollup_score` (top ~20 IMOs of 99) — automatic inclusion
- Tier 2: any IMO scoring above adjacent threshold (refined by ws CTO REPAIR-AMENDMENT (b)(i) W1 threshold semantics; provisional = `rollup_score ≥ 50`) AND with explicit Series-license term match (i.e., Series 7/24/63/65/66/79 appears in `term_matches[]`) — included even if outside top quintile

Phase 2A subset size estimate: ~15-30 IMOs depending on Phase 1 distribution.

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import on all bronze/silver/gold scripts; ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** Andrew Q1 ratify text quoted verbatim in TO close session log (proves subset definition is operating from ratified rule, not COO speculation).
- **AC3.** Phase 2A subset selection algorithm applied against `serving/scoring.json` (Phase 1 ranked output post `.023` ship) emits `data/find/imo/config/phase2a-subset-{run-date}.json` listing the N selected IMOs with rationale (top-quintile vs adjacent+Series).
- **AC4.** LushaAI integration: per-IMO Lambda invocation on `find-insure-crawl-linkedin` (or equivalent Lusha-client Lambda from `.011` ship) — execute Lusha Search by company name → Prospecting filter to decision-relevant titles (CIO + portfolio-mgr + investment-committee + wealth-advisor + RIA-principal + Series-license-holder per scoring-weights-v0.1.json title_seniority_class_weights) → Enrich per-person for Series-license + tenure + title-seniority + LinkedIn-summary keywords.
- **AC5.** Per-IMO silver emit: `corp/{slug}/silver/linkedin/{run-date}/{lusha_person_id}.json` per medallion convention; Rule 17 strict passthrough of Lusha response fields (no field-pruning; flag-pattern for missing optional fields per `.005` precedent).
- **AC6.** Per-IMO gold emit: `corp/{slug}/gold/linkedin/{run-date}/employees.json` with structure `{run_date, taxonomy_version, employees: [{lusha_person_id, name, title, title_seniority_class, series_licenses[], tenure_years, employee_score, keyword_matches}, ...], employee_count, top_employee_score, series_density}`. Decision-useful per CVO M1 framework.
- **AC7.** Cost-gate per PRD §3.7: LushaAI per-IMO Lambda timeout per PRD §3.8 (20-call hard-cap + soft-abort per IMO); cumulative cost monitored via CloudWatch; sns:Publish alert if Phase 2A cumulative exceeds COO ceiling (recommend $30 ceiling for ~30-IMO subset with $5 alert threshold; refine post-`.011` Lusha-rate-card empirical).
- **AC8.** Andrew Q1 EDGE CASE handling: if Phase 1 ranked output produces fewer than 5 top-quintile IMOs (e.g., highly-skewed distribution) → escalate to ws CTO for subset-rule re-evaluation before dispatch. If empty subset → surface to ws COO with `[PHASE2A-EMPTY-SUBSET]` finding (likely indicates Phase 1 calibration miss; route to W1/W2 taxonomy refinement).
- **AC9.** GDPR opt-out compliance per `.011` AC5: pre-flight check against opt-out DDB table (`find_insure_opt_out`); skip any Lusha person ID present in opt-out registry. Per opt_out_webhook_receiver.py scaffold ratify post-`.011` ship.
- **AC10.** `comp-iam service find-insure-crawl-linkedin` (or final Lambda name) no MISSING + `comp-pipescript deployed` MATCH + `comp-blast` no unexpected downstream.

## Dependencies

- **FIND_INSURE.011 RAVC2-Accept** — HARD GATE. Lambda skeletons + lusha_client.py + opt_out_webhook_receiver.py all must be shipped + AE-deployed before this TO executes.
- **Andrew Q1 sovereign ratify (subset-cut rule)** — HARD GATE. Without explicit Andrew rule, COO will not author `phase2a-subset-{run-date}.json` per LD-0090 sovereign-class decision class.
- **FIND_INSURE.023 RAVC2-Accept (serving/scoring.json)** — RECOMMENDED but not strictly hard-gate. AC3 reads serving/scoring.json; if .023 hasn't shipped, you fall back to reading per-IMO `gold/score.json` files + computing the ranking inline (degraded path; flag to ws COO).
- **AE 0.7 deploy substrate** — LushaAI Lambdas need deployment via find-insure Terraform module + `imo-pipeline-v0.X.0` tag bump.
- **LushaAI API key** — landed pre-reboot in Secrets Manager `find-insure/lusha-ai/api-key` per AE 0.7 SYNC handoff.

## Sequencing — staged pending gates

**Pre-gate (NOW; pre-stage design):**
1. ~1h: read `.011` design (post-ship) + Lusha API v3 reference doc + this TO + ws CTO REPAIR-AMENDMENT (b)(i) (when landed)
2. ~1h: author design brief at `.../deliverables/phase2a_live_dispatch_design_v0.1.md` — subset-selection-algorithm pseudocode + per-IMO Lusha-invocation pattern + cost-budget model

**Post-gate (when GO fires):**
3. ~30min: Andrew Q1 rule + Phase 1 `serving/scoring.json` → emit `phase2a-subset-{run-date}.json`
4. ~2-3h: per-IMO LushaAI invocation + silver/gold emit
5. ~30min: AC6 spot-check + AC7 cost-confirm
6. ~15min: commit + RAVC2-Request

**Total ETA:** ~5h wall post-gate-clear; ~2h pre-gate authoring (concurrent with `.011` ship + Phase 1 close window).

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.024 — Phase 2A LIVE-DISPATCH LushaAI enrichment` to ws COO. CC ws CTO + ws CVO. Body: code commit hash + subset-config hash + per-IMO LushaAI evidence sample + employee-score top-5 (visual inspect; should match CIO/portfolio-mgr/etc. expected title classes) + cost-gate compliance + comp-iam/comp-pipescript outputs.

## Sister coord

- **FIND_INSURE.011 (your prior staged TO)** — your skeleton bundle ships first; this TO consumes the ship.
- **FIND_INSURE.025 (Phase 2B Stage Bα HAR parser; DS~D)** — parallel-or-sequential per ws CTO sequencing; if Phase 2A + 2B run in parallel, your LushaAI subset is independent of Stage Bα job-postings subset (Phase 2B has its own per-board ranking criteria).
- **DS~E .023 serving consolidation** — your gold/linkedin/employees.json output feeds the Phase 3 `serving/employees.json` consolidated table per .023 forward-staging.

## Notes

- Per [[feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch]]: pre-stage design + subset-selection-algorithm pseudocode + per-IMO Lambda invocation pattern NOW so the gate-flip moment fires immediately.
- Per [[feedback_silver_no_field_slimming]] / Rule 17: silver passthrough Lusha response fields strict — gold is where business-logic filtering happens (e.g., title-seniority weighting).
- Andrew Q1 EDGE CASE (AC8) handles the "Phase 1 calibration miss" class — important defensive surface.
- Cost-gate ceiling $30 is COO conservative provisional; refine post-`.011` ship when Lusha rate-card is empirically known.

— ws COO /drive cycle 165 forward-staging — Phase 2A LIVE-DISPATCH pre-author 2026-05-27T~23:14Z
