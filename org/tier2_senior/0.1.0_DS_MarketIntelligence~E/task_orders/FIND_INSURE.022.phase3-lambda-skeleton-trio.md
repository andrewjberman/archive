# FIND_INSURE.022 — Phase 3 Lambda skeleton trio + silver-gold contract ref doc

| | |
|---|---|
| **Project** | FIND_INSURE (Phase 3 pre-authoring) |
| **Owner** | 0.1.0_DS_MarketIntelligence~E |
| **Authored** | 2026-05-27T~21:15Z (2.0.0_SA_COO /drive cycle #188) |
| **GO** | YES — dispatch_held=false |
| **Status** | complete (trio shipped work-cycle:0003+0004: AC-B3 build_scoring_serving 650b0714e + AC-B1 build_companies_serving 87c28cfdf + AC-B2 build_employees_serving; AC-B4 silver-gold contract prior 180b4c21e/d4eeba04c; AC-B5 gate clean; AC-B6 test-count proportional-to-skeleton-surface, scales at build-moment) |
| **Authority** | Brief `b67ad03ec` (docs/briefs/find-insure-phase3-ir-feedback-and-lambda-skeleton-20260527.md) + Andrew sovereign 2026-05-27T~19:50Z pace-pickup + ws COO greenlight 20:03Z |
| **Sequencing** | Fully parallel to Phase 1 + Phase 2A critical paths; skeleton authoring against fixture JSON (mirrors DS~A `.005` + DS~B `.006` + DS~C Phase 2A skeleton pattern) |

## Scope

Brief b67ad03ec Thread B — author 3 Phase 3 serving Lambda skeletons against fixture JSON + silver-gold contract reference doc.

## Acceptance criteria (Thread B from brief §3)

- **AC-B1**: `data/find/imo/scripts/serving/build_companies_serving.py` skeleton + unit-tests against fixture gold-tier JSON. Per PRD v0.6 §4 Phase 3 deliverable 1 (`companies` table).
- **AC-B2**: `data/find/imo/scripts/serving/build_employees_serving.py` skeleton + GDPR opt-out propagation logic + unit-tests. Per PRD v0.6 §4 Phase 3 deliverable 1 (`employees` table).
- **AC-B3**: `data/find/imo/scripts/serving/build_scoring_serving.py` skeleton + time-travel archive emission per PRD v0.3 §3.2 Q-B + unit-tests. Per PRD v0.6 §4 Phase 3 deliverable 1 (`scoring` table).
- **AC-B4**: `docs/reference/find-insure-silver-gold-contract.md` — NEW reference doc (sister to `lusha-api-v3.md` pattern); silver/gold schema contract emerging from DS~A `parse_web_silver.py` + DS~B `score_web_gold.py` + DS~C `score_linkedin_gold.py` substrate. **GREENLIGHTED for speculative pre-authoring per COO MCP `20260527T205907Z` cycle #187** — may already be in flight.
- **AC-B5**: `ds-commit-gate.sh` exit 0 on all new `.py` files (py_compile + ds-precommit-check + ruff per Rule 14 + Rule 15 future-annotations enforced)
- **AC-B6**: Target 35-50 self-test cases per module mirroring DS~A + DS~B + DS~C discipline

## Brief reference

Full scope at `docs/briefs/find-insure-phase3-ir-feedback-and-lambda-skeleton-20260527.md` §2.2 + §3 Thread B ACs. Per-module fixture-JSON contract + cost-gate + KMS integration + empty-IMO edge case all detailed in brief §2.2.

## Non-scope (v0.1 skeleton)

- NO live S3 cross-IMO scan (skeleton fires against fixture JSON only)
- NO Phase-2A-subset-not-met live empirical (brief §B.4 handles via skeleton branch)
- NO production-fixture data
- NO Lambda packaging / TF authoring / AWS deploy (this TO is skeleton + tests only; AE 0.7 handles packaging when Phase 1+2A converge and skeleton lands on real data)

## Cost-gate + KMS integration

Per brief §B.4:
- Lambda init reads `find-insure-cost-state` DDB (minor read; Phase 3 doesn't burn Lusha/Bright-Data credits but tracks own S3 GET + parquet write costs)
- `find-insure-lambda-role` auto-gets KMS Decrypt grant on serving/* per PRD v0.4 §3.1
- Schema version stamp `schema_version: "v1.0"` per Q-S1 disposition

## Sister-coord

CC DS~A + DS~B + DS~C on AC-B4 silver-gold contract — they validate the contract describes their existing outputs accurately. If they flag inaccuracy (post-Phase-1+2A empirical), v0.2 follow-up TO authored — NOT a Phase 1 retrofit.

## RAVC2-expected window

~4-6h wall (3 Python modules + 35-50 tests each + AC-B4 reference doc). RAVC2-Request to ws COO with AC-B1..B6 self-attestation table + cite all module paths + cite `ds-commit-gate.sh` exit 0.

## Sister TO

`FIND_INSURE.021` (Thread A IR-team feedback protocol design) dispatched same cycle. Author in parallel OR sequentially per your discretion.

— 2.0.0_SA_COO /drive cycle #188 same-cycle dispatch
