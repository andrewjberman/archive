# FIND_INSURE.030 — Gold-tier score_class field (DS~A)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.7+ §3.6 gold tier + CVO 11-axes verdict `54ace66c8` §G1 observation
**Pod:** 0.1.0_DS_MarketIntelligence~A
**Lane:** DS_MarketIntelligence ~A (Phase 1 gold-tier follow-on)
**Issued to:** 0.1.0_DS_MarketIntelligence~A
**Author:** 2.0.0_SA_COO 2026-05-28T~00:10Z (/drive cycle 167 redirect per Step 2b.4 Andrew directive)
**Sizing:** ~45-60min wall (small ADDITIVE patch + 3 unit-tests + empirical re-run against existing 13 IMOs)
**Authority anchor:** CVO 11-axes verdict §G1 observation 2026-05-27T~21:00Z + Andrew goal-set 22:49Z drive-end-to-end + Andrew 23:25Z parallelize + /drive Step 2b.4 "standing-by terminal state never acceptable"

<status>complete</status>

## Objective

Patch `data/find/imo/scripts/gold/score_web_gold.py` (~326L) to add `score_class` enum field per CVO §G1 finding. Disambiguates the gold-zero overload: distinguishes "scanned content has no AM signal" (true zero; signal-class) from "no content was scanned" (data-quality issue). An IR analyst handed the consolidated ranked table can now distinguish a 0-score that means "this IMO is insurance-only no-AM" from a 0-score that means "we couldn't read their site."

**The 3 score classes:**

| value | criterion | example |
|---|---|---|
| `SCORED` | `page_count_scanned > 0` AND silver has no `blocked_reason` non-null AND term-extraction ran normally | Avantax (rollup=100 with 171 matches); 1st-Atlantic (rollup=0 with 0 matches on 5 SUCCESS pages — true-negative); Allianz (rollup=100 with 565 matches — W1-FP-class but signal-class data quality) |
| `BLOCKED_UPSTREAM` | silver has `blocked_reason` non-null (empty-body, robots-block, fetch-timeout, etc.) AND `page_text/body_text` is null | Carl-Ostenson (silver `blocked_reason: empty-body`, `body_text: null`); Stage 1 robots-blocked IMOs |
| `NO_PAGES` | `page_count_scanned == 0` (bronze never produced any silver records OR silver records all have blocked_reason) | (rare; Stage 2 dispatch miss) |

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import; `.tools/ds-commit-gate.sh` clean (py_compile + AST + ruff py39); CLAUDE.md Rule 14 + Rule 15 compliance.
- **AC2.** `score_class: str` field added to gold record schema. Position: between `rollup_score` (existing) and `scored_at` (existing) per readability hint. Existing 12-field gold schema → 13-field gold schema. Per CLAUDE.md Rule 17 spirit applied to gold layer (no field-pruning; ADDITIVE).
- **AC3.** Derivation logic in `score_imo()` (or wherever the gold record is finalized):
  - SCORED = `page_count_scanned > 0` AND (any silver record exists with non-null `body_text`/`page_text`)
  - BLOCKED_UPSTREAM = `page_count_scanned > 0` AND (all silver records have `blocked_reason` non-null OR all have null `body_text`)
  - NO_PAGES = `page_count_scanned == 0`
  - **Tie-breakers** for edge cases:
    - Mixed silver (some SUCCESS + some BLOCKED) → SCORED (signal class wins; per "majority" rule OR "any SUCCESS counts" — your judgment, default `any SUCCESS counts` per minimal-loss-of-information)
    - All `page_count_scanned > 0` but `term_matches[] == []` → SCORED (this IS true-negative on SUCCESS-class silver; Avantax's 1st-Atlantic anchor is this case)
- **AC4.** ADDITIVE strict: no signature regression on existing gold record keys; existing consumers (Phase 3 `.023` serving consolidation, `.022` trio, DS~E silver-gold contract `180b4c21e`) read existing keys unaffected; new `score_class` field is unknown-but-additive to existing consumers.
- **AC5.** Empirical re-run against existing 13 IMO universe (3 original + 10 Stage 1):
  - **Original 3:**
    - Avantax = `SCORED` (rollup=100, 171 matches) ✓ expected
    - 1st-Atlantic = `SCORED` (rollup=0, 0 matches on 5 SUCCESS pages — true-negative) ✓ expected
    - Carl-Ostenson = `BLOCKED_UPSTREAM` (silver `blocked_reason: empty-body`) ✓ expected
  - **Stage 1 (post-W1-refinement re-grade pending; current state at .030 ship moment):**
    - Cambridge IR = `BLOCKED_UPSTREAM` if silver shows SPA-class fetch (likely) OR `SCORED` if silver had any SUCCESS pages
    - D.A. Davidson + Lincoln Financial + Structured AM + Liberty Bankers + Preferred Annuity = `BLOCKED_UPSTREAM` (robots-blocked)
    - Lincoln Investment + Allianz Life + American Equity Life + Midland National = `SCORED` (signal-class data quality; their W1-FP issue is separate)
- **AC6.** Self-test extend with 3 new cases per class (1 SCORED + 1 BLOCKED_UPSTREAM + 1 NO_PAGES) using synthetic silver fixtures.
- **AC7.** `comp-pipescript io data/find/imo/scripts/gold/score_web_gold.py` clean (or "Unknown script" per .005/.007 precedent — comp-graph rebuild lag; tooling-not-correctness).
- **AC8.** AE 0.7~A combined Stage 2 cycle sister-deploy ABSORBS gold redeploy. Tag bump: `imo-pipeline-v0.4.1` (patch-level on score-web v0.4.0 baseline) folded into AE 0.7~A's combined safe-apply window (W1 refinement re-deploy + .026 telemetry + .007 AC7 parse-web v0.3.1 + AC-T2 escape-valve if ready + your .030 score-web v0.4.1). **Sister-coord with AE 0.7~A** via inbox MCP at your ship moment so they fold .030 into their next safe-apply.
- **AC9.** Sister-coord with DS~E `.023`: align `data_quality_class` enum semantics so values are cross-tier-compatible (silver-tier `blocked_reason` → gold-tier `score_class` → serving-tier `data_quality_class` form a consistent enum family). DS~E pre-staging .023 design + code per ws COO 22:59Z STAGED dispatch; coordinate enum-values via MCP at your draft-of-AC3 moment.

## Dependencies

- **FIND_INSURE.006 RAVC2-Accept (gold score-web shipped)** — landed pre-reboot at commit `877ca495d`; .030 is ADDITIVE patch.
- **FIND_INSURE.007 RAVC2-Accept (Rule 17 silver passthrough)** — landed at `3ee6ee869`; silver now carries 5 bronze meta fields including `http_headers` + `tls_fail_original` for diagnostic; your `score_class` derivation may also surface `blocked_reason_detail` from `http_headers` in v0.2 (out-of-scope this TO).
- **No PRD-amend dependency.** Per CVO §G1 "v2 candidate" framing; this TO closes the G1 observation execution leg. PRD §3.6 gold-tier amend optional (ws CTO discretion).
- **AE 0.7~A `.026` telemetry-emit** — parallel-not-blocking. If .026 ships before .030, your gold record can optionally include telemetry context (out-of-scope).
- **DS~E `.023`** — sister-coord for enum-values alignment (AC9).

## Sequencing — fast-turnaround follow-on

1. ~5min: read CVO §G1 finding (anchor) + your prior `.007` patch pattern + `score_web_gold.py` `score_imo()` + silver schema (you authored)
2. ~10min: patch `score_imo()` to derive `score_class` from silver state inspection + add field to gold record
3. ~5min: ds-commit-gate + ruff + py_compile
4. ~10min: extend self-test fixture with 3 new cases
5. ~10min: local invocation against 3-IMO baseline + spot-check Carl-Ostenson = BLOCKED_UPSTREAM
6. ~5min: sister-coord MCP to DS~E (AC9 enum alignment) + AE 0.7~A (AC8 sister-deploy)
7. ~5min: commit + RAVC2-Request

**Total ETA:** ~45-60min wall from .030 pickup.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.030 — Gold-tier score_class field` to ws COO. CC ws CTO + ws CVO (closes CVO §G1 observation execution leg) + DS~E (AC9 enum sister-coord) + AE 0.7~A (AC8 sister-deploy coord). Body: commit hash + diff summary (3-class derivation logic + field-add lines) + AC5 empirical evidence (13-IMO score_class distribution table) + AC6 self-test pass count + AC9 sister-coord ack from DS~E + comp-pipescript output.

## Compiler tools mandate

- **Before edit:** `comp-pipescript io data/find/imo/scripts/gold/score_web_gold.py` (likely "Unknown script" per .005 precedent)
- **Before commit:** `.tools/ds-commit-gate.sh data/find/imo/scripts/gold/score_web_gold.py` mandatory per Rule 14
- **After AE deploy (AC8):** `comp-pipescript deployed find-insure-score-web` MATCH gate before any production re-run

## Cross-domain coordination

`<minimal/>` — silver→gold layer; no cross-domain S3 artifact overlap with other active TOs. AE 0.7~A combined Stage 2 cycle absorbs deploy (your AC8); DS~E .023 enum alignment is informational sister-coord (your AC9). FIND_INSURE.008 universe-run will produce gold records with `score_class` populated once .030 ships + AE redeploys.

## Notes

- Per CVO §G1: "Recommend gold add field `score_class: {SCORED, BLOCKED_UPSTREAM, NO_PAGES}` or similar to distinguish. Not critical-block but worth banking as v2 candidate." This TO closes the v2 candidate at v0.4.1 patch level — Phase 1 RAVC2-Accept can now grade G1 ACCEPTED (currently B+ per CVO Mode B).
- Per [[feedback_silver_no_field_slimming]] / Rule 17 — patch is ADDITIVE not slim; respects discipline at gold layer.
- Per Andrew goal-set drive-through-Phase-3 + 23:25Z parallelize — your DS~A bandwidth is FIND_INSURE-prioritized; .030 is the cleanest next-action that closes a CVO observation.
- Per DS~A self-flag in .007 RAVC2-Receipt 23:12Z: "ready for: ... (c) any FIND_INSURE.007 sister patch class (e.g., gold-tier `score_class` field surface candidate flagged in CVO §G1 observation)." This TO realizes that surface; banking [[feedback_dsa_self_flagged_sister_patch_pattern]] if first-fire (or skipping if not novel).

— ws COO /drive cycle 167 redirect 2026-05-28T~00:10Z
