# FIND_INSURE.011 — Phase 2A Lambda skeleton bundle (DS~C)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.5 §4 Phase 2A
**Brief:** `docs/briefs/find-insure-phase2a-lambda-skeleton-design-20260527.md` (`e3fcefba9` ws CTO)
**Pod:** 0.1.0_DS_MarketIntelligence~C
**Lane:** DS_MarketIntelligence ~C (Phase 2A LinkedIn-pipeline skeleton authoring)
**Author:** 2.0.0_SA_COO 2026-05-27T~20:02Z (cycle #186 pace-pickup per Andrew sovereign 19:50Z)
**Status:** complete — all 5 ACs MET; RAVC2-Request fired `20260528T0035Z` (cycle 3); awaiting COO RAVC2-Accept (= .024 Gate 1). Self-flip active->complete on RAVC2-Request per worker discipline. Full phase2a suite green post `4d620cd71` (stale .034-orphaned integration test repaired ~C cycle 1).
**Sizing:** ~2-4h wall (5 modules + 35-50 unit-tests per module = 175-250 unit-tests; STANDBY-PREP class)

<status>complete</status>

---

## Objective

Author Phase 2A LinkedIn-pipeline Lambda skeletons + shared Lusha-client utility + GDPR opt-out webhook receiver scaffold against fixture JSON. STANDBY-PREP class — code structure + unit-tests ONLY. **DO NOT** make live Lusha API calls / DDB writes / SNS publishes / AWS deploys.

Substrate fires the moment all 3 gates clear:
- Phase 1 RAVC2-Accept (ETA ~19:35-20:00Z)
- KMS+DDB+SNS apply (`imo-pipeline-v0.5.0` Andrew sovereign-binds in route)
- Andrew subset-cut decision for v0.6.0 first-run

## Deliverables (5 modules + unit-test suite)

1. `data/find/imo/scripts/bronze/crawl_linkedin_bronze.py` — crawl Lambda skeleton (Bright Data scraping_browser1 zone via Lusha-resolved LinkedIn URL)
2. `data/find/imo/scripts/silver/parse_linkedin_silver.py` — parse Lambda skeleton (Lusha-format JSON → silver per medallion)
3. `data/find/imo/scripts/gold/score_linkedin_gold.py` — score Lambda skeleton (named-individuals + Series-license counts + AUM extraction)
4. `data/find/imo/scripts/_util/lusha_client.py` — shared Lusha API v3 utility (endpoint mapping + rate-limit per `docs/reference/lusha-api-v3.md`)
5. `data/find/imo/scripts/bronze/opt_out_webhook_receiver.py` — GDPR opt-out webhook receiver scaffold (DDB cost-state mocked + flag for downstream Phase 2A Lambda skip-list)

**Test fixtures:** `data/find/imo/tests/fixtures/phase2a/` (you author alongside the modules).

## Acceptance criteria

- **AC1.** `crawl_linkedin_bronze.py` Lambda skeleton + handler signature + fixture-based 5-7 unit-tests covering Bright Data scraping_browser1 invocation pattern (URL → raw HTML → S3 PutObject bronze).
- **AC2.** `parse_linkedin_silver.py` Lambda skeleton + handler signature + fixture-based 5-7 unit-tests covering Lusha JSON shape → silver schema mapping. Coordinate with DS~A `.005` silver-side guidance per `[[feedback_silver_no_field_slimming.md]]` (Rule 17 preserve-all).
- **AC3.** `score_linkedin_gold.py` Lambda skeleton + handler signature + fixture-based 5-7 unit-tests covering named-individuals extraction + Series-license counts + AUM number extraction. Phase 3 sees these as enrichment dimensions per CVO Tier 1 Item #1 saturation-resolution recommendation.
- **AC4.** `lusha_client.py` shared utility + endpoint mapping + rate-limit handling + 10-15 unit-tests against mocked Lusha response fixtures.
- **AC5.** `opt_out_webhook_receiver.py` GDPR webhook scaffold + DDB write-pattern (mocked) + 3-5 unit-tests.
- **AC6.** `from __future__ import annotations` first line of every gold/silver/bronze script per Rule 15. Universal-extractor + sister `_util/lusha_client.py` no `from __future__` requirement (rule applies to data/*/scripts/{gold,silver,bronze}/*.py only).
- **AC7.** Pre-commit gate via `.tools/ds-commit-gate.sh` clean on all 5 files; commit via `.tools/safe-commit.sh --author "0.1.0_DS_MarketIntelligence~C <0.1.0_DS_MarketIntelligence~C@opal.agent>"`.

## Sister-coord opportunities

- **DS~A** — silver schema patterns from `.005` (LOCK v0.2.1 canonical; body_text:null symmetric per `f7e61aa39`)
- **DS~B** — gold scoring patterns from `.006` (taxonomy-driven term-matching; rollup_score formula)
- **DS~D** — Phase 2B job-board public-API survey (FIND_INSURE.016) shares `lusha_client.py` pattern conceptually — your shared utility informs their per-board client design

## Lane discipline

- `data/find/imo/scripts/{bronze,silver,gold,_util}/**` — your DS-lane scope; ~C author authority confirmed via owned-paths permitted_agents

## RAVC2 trigger

RAVC2-Request fires when:
- All 5 modules authored + AC1-AC7 self-attested PASS
- Pre-commit gate clean
- 1 commit per module OR 1 bundle-commit (your call; smaller commits preferred for review-grain but bundle acceptable)

## Self-classification per /work LD-0072

If blockers surface (e.g., Lusha API shape ambiguity in `docs/reference/lusha-api-v3.md`, silver schema patterns unclear, etc.): `[BLOCKED-ASK]` to COO per LD-0116 chain-of-command.

CC: 1.0.0_SA_CTO (brief author + design authority) + 0.1.0_DS_MarketIntelligence~A (silver-side sister-coord) + 0.1.0_DS_MarketIntelligence~B (gold-side sister-coord) + 0.1.0_DS_MarketIntelligence base (parent lane visibility)
