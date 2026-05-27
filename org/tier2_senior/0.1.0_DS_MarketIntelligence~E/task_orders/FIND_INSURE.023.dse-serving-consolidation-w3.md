# FIND_INSURE.023 — serving consolidation W3 (Phase 3 enabling — staged)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4 §4 Phase 3 deliverable 1 (consolidated IR-team-facing target tables)
**Pod:** 0.1.0_DS_MarketIntelligence~E (primary) + ~B (co-author optional for parallel partitioning)
**Lane:** DS_MarketIntelligence ~E (Phase 3 serving-tier authoring)
**Issued to:** 0.1.0_DS_MarketIntelligence~E
**Author:** 2.0.0_SA_COO 2026-05-27T~22:55Z (cycle 165 post-reboot Phase 1 close-gating triad)
**Sizing:** ~3-5h wall (Lambda authoring + unit tests + empirical run against 99-IMO universe output post-.008 close)
**Authority anchor:** CVO /verify-channel verdict `54ace66c8` §W3 INCOMPLETE — "NO consolidated serving/scoring.json exists; CONDITIONAL on C1 + Phase 1 close + consolidation TO" + Andrew sovereign goal-set 2026-05-27T~22:49Z (drive FIND_INSURE end-to-end through Phase 3 close); CVO P2 priority routed via COO 21:00Z mandate.

<status>staged</status>
<dispatch_held>true</dispatch_held>
<dispatch_unlock_gate>FIND_INSURE.008 AC7 RAVC2-Accept (99-IMO universe-run complete + 99 gold/score.json files exist)</dispatch_unlock_gate>

## Objective

Author the `serving-consolidate` Lambda that reads all 99 per-IMO `gold/web-scrape/{run-date}/score.json` files and emits the consolidated `serving/scoring.json` ranked scoring table for IR-team consumption. This is the **W3 axis empirical close** per CVO 11-axes verdict — without this deliverable, FIND_INSURE Phase 1 cannot grade beyond INCOMPLETE on W3, and Phase 3 cannot fire.

**Output shape (initial v0.1; refine per IR-team-individual feedback per CVO ADDITIVE-1 pre-Phase-3 gate):**

```json
{
  "schema_version": "v0.1",
  "run_date": "YYYY-MM-DD",
  "scored_at": "ISO8601 UTC",
  "taxonomy_version": "v1",
  "weights_config_version": "v0.1",
  "universe_size": 99,
  "scored_count": <int>,
  "blocked_count": <int>,
  "ranked_companies": [
    {
      "rank": 1,
      "company_slug": "avantax-wealth-management",
      "rollup_score": 100,
      "rollup_raw": 28.13,
      "class_diversity_multiplier": 1.4,
      "term_match_count": 171,
      "term_class_distribution": {...},
      "page_count_scanned": 5,
      "page_count_with_matches": 5,
      "wm_classification": "PRESENT|ADJACENT|ABSENT",
      "top_signals": [<top-5 term_matches with context_snippet>],
      "stage1_validation_status": "in-subset|not-in-subset",
      "data_quality_class": "SCORED|BLOCKED_UPSTREAM|NO_PAGES"
    },
    ...
  ]
}
```

**`wm_classification` field is gated** on ws CTO REPAIR-AMENDMENT (b)(i) ratifying threshold semantics for present / adjacent / absent labels. If CTO PRD amend lands before this TO ships, encode per amended spec. If not, emit continuous `rollup_score` + leave `wm_classification: null` with audit field `wm_classification_reason: "PRD spec pending CTO Trigger-2(b)(i) REPAIR-AMENDMENT"`.

**`data_quality_class` field** distinguishes the CVO §G1 finding (overloaded zero — `score=0` from no-AM-signal vs from EMPTY-BODY upstream): SCORED = page_count_scanned>0 AND page_count_with_matches=0 (true zero); BLOCKED_UPSTREAM = bronze EMPTY-BODY / silver BLOCKED record present; NO_PAGES = no bronze pages crawled (Stage 2 dispatch miss).

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import; ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** Lambda code at `data/find/imo/scripts/serving/consolidate_scoring.py` (medallion-by-layer per CTO ARCH-RULING; serving-tier is the new layer for cross-IMO aggregations).
- **AC3.** Lambda handler `lambda_handler(event, context)` with event `{run_date, [universe_bucket], [output_bucket], [output_prefix]}` → returns `{universe_size, scored_count, blocked_count, ranked_count, output_key, started_at, ended_at, duration_ms}`.
- **AC4.** Reads ALL `corp/{slug}/gold/web-scrape/{run-date}/score.json` files via S3 list + per-file get; handles missing files (Stage 2 dispatch miss) by setting `data_quality_class: NO_PAGES` in the ranked entry (not skipping).
- **AC5.** Ranking: sort descending by `rollup_score`, ties broken by `term_match_count` (desc) then `page_count_with_matches` (desc) then `company_slug` (asc for stable). Rank field is the post-sort 1-indexed position.
- **AC6.** Top-5 signals per company: read first 5 entries from `term_matches[]` in the gold/score.json (already ordered by gold's per-match scoring); preserve context_snippet + location_class + term + class. Decision-useful for IR-team spot-check.
- **AC7.** History archive per PRD Q-B: write `serving/_history/scoring/{run-date}.json` (in addition to the current-state `serving/scoring.json` overwrite-in-place) so prior run-dates are auditable. History-class only for scoring.json per Q-B ruling.
- **AC8.** Empirical run: invoke against the 99-IMO universe-run output (post-.008 AC7 close); confirm:
  - `universe_size: 99`, `scored_count + blocked_count = 99`, `ranked_count: 99` (NO_PAGES entries included in ranking with score=0 + data_quality_class set)
  - Top-5 companies + their `rollup_score` reasonable on visual inspection (Avantax-class candidates should be top quartile)
  - Bottom-5 companies are insurance-only known-absent IMOs (anti-pattern check: if a known-AM IMO from CTO's Stage 1 subset lands bottom-5, surface as W1/W2 calibration finding for next-cycle taxonomy refinement)
- **AC9.** Cost: serving-consolidate Lambda is single-invocation per run-date (NOT per-IMO); memory + timeout per AE deployment sizing — recommend 512MB / 5min initial.
- **AC10.** `comp-pipescript io data/find/imo/scripts/serving/consolidate_scoring.py` clean (after AE comp-graph registration TO if needed — coordinate with AE 0.7); `comp-iam service find-insure-serving-consolidate` confirms s3:GetObject (corp/*/gold/*) + s3:PutObject (serving/* + serving/_history/scoring/*) scope.

## Dependencies

- **FIND_INSURE.008 AC7 RAVC2-Accept** — HARD GATE. Universe-run output (99 gold/score.json files) is the input contract. Until .008 closes, this TO stays staged.
- **FIND_INSURE.007 RAVC2-Accept** — NOT a hard gate. Rule 17 silver-extension is upstream of gold; gold/score.json shape is unchanged by .007. But if .007 ships before .008 universe-run completes, the 99 silver records will carry the 5 extra fields — consumed downstream by Phase 3 enrichment Lambdas (.022 trio), not by .023 itself.
- **AE 0.7 Lambda deploy substrate** — serving-consolidate Lambda needs deployment via the existing find-insure Terraform module; sister AE deploy TO if AE 0.7 is bandwidth-constrained. If you ship the Python code + IAM additions cleanly, AE 0.7's deploy cycle picks it up in routine course.
- **ws CTO REPAIR-AMENDMENT (b)(i) on W1 threshold semantics** — gates the `wm_classification` field. If amend not landed at AC8 empirical run, ship with `wm_classification: null` + reason field; do NOT block .023 on the amend. Forward-class issue.
- **CVO ADDITIVE-1 IR-team-individual identification** — pre-Phase-3 gate per CVO Mode B verdict `a5920688c`. .023 ships the consolidation; IR-team sign-off on the consolidated output is a separate close-gate moment (handled via .021 IR-team feedback protocol TO already authored in DS~E lane).

## Sequencing — staged pending .008 close

**Pre-.008-close (NOW; pre-stage your design):**
1. ~30min: read CVO 11-axes §W3 + §G1 (data_quality_class motivation) + PRD §3.6 serving layer + design brief authoring pattern from .022 Phase 3 Lambda skeleton trio (DS~E's prior staged TO)
2. ~1h: author design brief at `org/tier2_senior/0.1.0_DS_MarketIntelligence~E/deliverables/serving_consolidate_design_v0.1.md` — schema, ranking logic, history-archive structure, wm_classification handling logic (dual-path for spec-pending vs spec-landed)
3. ~1h: code Lambda against design + unit tests against synthetic 5-IMO gold fixture (covers SCORED + BLOCKED_UPSTREAM + NO_PAGES classes)
4. **GATE — wait for FIND_INSURE.008 AC7 close**

**Post-.008-close (when GO signal fires):**
5. ~30min: AC8 empirical run against real 99-IMO universe output + spot-check
6. ~30min: AE 0.7 SYNC for Lambda deploy + comp-iam confirmation
7. ~15min: commit + RAVC2-Request

**Total ETA:** ~3-4h pre-gate code + design + tests + ~1-2h post-gate empirical + deploy = ~5h total wall, dominated by code-and-test phase.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.023 — serving consolidation W3 (Phase 3 enabling)` to ws COO with: code commit hash + design brief reference + unit test results + AC8 empirical evidence (top-5 + bottom-5 + scored/blocked/no-pages distribution) + comp-iam confirmation + sister coordination with AE 0.7 (deploy) + sister coordination with DS~E (.021 IR-team feedback protocol — for downstream Phase 3 close gate). CC ws CTO + ws CVO. **This is the Phase 3 substantive deliverable; AC8 PASS + CVO Mode B comprehensive verdict + IR-team sign-off via .021 = Phase 3 RAVC2-Accept → project close.**

## Compiler tools mandate

- **Before edit:** `comp-pipescript io` (will be "Unknown script" — pre-impl; document)
- **Before commit:** `.tools/ds-commit-gate.sh data/find/imo/scripts/serving/consolidate_scoring.py` mandatory per CLAUDE.md Rule 14
- **After commit + AE deploy:** `comp-pipescript deployed find-insure-serving-consolidate` MATCH + `comp-iam service` no MISSING

## Cross-domain coordination

- **.008 Stage 2 output** = your AC4 read contract (99 gold/score.json files)
- **.022 Phase 3 Lambda skeleton trio (DS~E pre-staged)** = parallel-or-sister; if .022 absorbs serving-tier scope, this TO MAY be redundant or partial-fold — read .022 spec first; surface to ws COO if scope overlap detected
- **.021 IR-team feedback protocol (DS~E pre-staged)** = your output is .021's input contract; coordinate schema-stability discipline (no breaking changes to serving/scoring.json schema without .021 sign-off)
- **ws CTO REPAIR-AMENDMENT (b)(i) on W1 threshold** = parallel; affects your wm_classification field only; do NOT block

## Notes

- Per CVO §W3 finding: "W3 CONDITIONAL. Until consolidation lands, 'ranking output' is a per-IMO score-file enumeration only." This TO is the structural close for W3.
- Per CVO §G1 G1-observation: "An IR analyst handed the 0-score ranking would not know the difference. Recommend gold add field `score_class: {SCORED, BLOCKED_UPSTREAM, NO_PAGES}` or similar to distinguish." Encoded as AC4 + AC8 via `data_quality_class` field — fixes the overloaded-zero class at the serving layer (cheaper than upstream gold-tier amend).
- Per [[feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch]]: pre-stage your design + code while .008 universe-run is in flight; this maximizes throughput-compression on the gate-flip.
- Per LD-0116 (Andrew sovereign 2026-05-27T~17:36Z) — no T2/3 ↔ MSTR direct comms; all blockers route via ws COO escalation ladder.

— ws COO /drive cycle 165 post-reboot Phase 1 close-gating triad 2026-05-27T~22:55Z
