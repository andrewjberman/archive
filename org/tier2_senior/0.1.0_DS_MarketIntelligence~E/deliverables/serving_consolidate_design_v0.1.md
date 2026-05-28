# FIND_INSURE.023 serving-consolidate design brief v0.1 (pre-stage)

| | |
|---|---|
| **Author** | 0.1.0_DS_MarketIntelligence~E |
| **Date** | 2026-05-28 |
| **Status** | DRAFT v0.1 — pre-stage design (TO dispatch_held on FIND_INSURE.008 AC7; design+code pre-stage authorized per ws COO 22:59Z + GO 04:36Z) |
| **TO** | `org/tier2_senior/0.1.0_DS_MarketIntelligence~E/task_orders/FIND_INSURE.023.dse-serving-consolidation-w3.md` |
| **PRD** | `docs/architecture/FIND_INSURE.md` v0.7.1 §4 Phase 3 deliverable 1 |
| **Authority** | CVO 11-axes `54ace66c8` §W3 INCOMPLETE + §G1 overloaded-zero + Andrew sovereign goal-set 2026-05-27T~22:49Z |

---

## §1 — Objective + W3 close context

Author the `serving-consolidate` Lambda (`data/find/imo/scripts/serving/consolidate_scoring.py`) that reads all 99 per-IMO `corp/{slug}/gold/web-scrape/{run-date}/score.json` files and emits the consolidated **`serving/scoring.json`** ranked scoring table — the canonical IR-team-facing ranked-companies artifact. This is the structural close for CVO §W3 ("Until consolidation lands, 'ranking output' is a per-IMO score-file enumeration only").

**Scope-disposition (Option iii, ws COO `034421Z`):** `serving/scoring.json` is THIS Lambda's canonical ranked-companies table. The `.022 build_scoring_serving` methodology artifact lives at `serving/_metadata/scoring_methodology.json` — distinct namespace, no collision. (`.022 build_companies_serving` writes `serving/companies.json`; this `.023` consolidate writes `serving/scoring.json`. Both are ranked tables but: companies.json = full company-row join across web+linkedin+job-posting; scoring.json = web-scrape score-file consolidation specifically for the W3 close. At Phase 3 convergence these may merge; v0.1 keeps them separate per the TO + .022 scope.)

---

## §2 — Input contract (gold/score.json)

Per DS~B `score_web_gold.py` (v0.7.1, FIND_INSURE.031). Each `corp/{slug}/gold/web-scrape/{run-date}/score.json` carries (fields consumed by consolidate):

```
{
  "slug": str,
  "rollup_score": int 0-100,
  "rollup_raw": float,
  "class_diversity": int,                  # NEW v0.7.1 (DS~B .031)
  "class_diversity_multiplier": float,
  "wm_classification": "present|adjacent|absent|null",  # NEW v0.7.1 (DS~B classify_wm())
  "wm_classification_reason": str|null,
  "term_match_count": int,
  "term_class_distribution": {class: count, ...},
  "page_count_scanned": int,
  "page_count_with_matches": int,
  "term_matches": [ {term, class, location_class, context_snippet, ...}, ... ],  # pre-ordered by gold per-match score
  "taxonomy_version": str,                 # expect "v2" post-.031
  "weights_config_version": str            # expect "v0.2" post-.031
}
```

**Version note:** the TO's illustrative schema shows `taxonomy_version: v1` + `weights_config_version: v0.1`, but DS~B `.031` ships against my `term-taxonomy-v2.json` + `scoring-weights-v0.2.json` (`4f557336b`). consolidate stamps the output with whatever versions the gold files carry (read-through, not hardcoded) + asserts consistency across the 99 files (surfaces a mixed-version warning if gold files disagree — a Stage-2 partial-redeploy signal).

---

## §3 — Output schema (serving/scoring.json)

```json
{
  "schema_version": "v0.1",
  "run_date": "YYYY-MM-DD",
  "scored_at": "ISO8601 UTC",
  "taxonomy_version": "<read-through from gold; expect v2>",
  "weights_config_version": "<read-through from gold; expect v0.2>",
  "universe_size": 99,
  "scored_count": <int>,
  "blocked_count": <int>,
  "no_pages_count": <int>,
  "wm_classification_distribution": {"present": <int>, "adjacent": <int>, "absent": <int>, "null": <int>},
  "ranked_companies": [
    {
      "rank": 1,
      "company_slug": "...",
      "rollup_score": 100,
      "rollup_raw": 28.13,
      "class_diversity": 3,
      "class_diversity_multiplier": 1.2,
      "term_match_count": 171,
      "term_class_distribution": {...},
      "page_count_scanned": 5,
      "page_count_with_matches": 5,
      "wm_classification": "present|adjacent|absent|null",
      "wm_classification_reason": null,
      "top_signals": [ <up-to-5 term_matches with context_snippet + location_class + term + class> ],
      "stage1_validation_status": "in-subset|not-in-subset",
      "data_quality_class": "SCORED|BLOCKED_UPSTREAM|NO_PAGES"
    }
  ]
}
```

Added beyond the TO sketch: `no_pages_count` + `wm_classification_distribution` (cheap aggregate stats that make the table self-describing for the IR analyst + feed the CVO Mode A §4 Stage-2 distribution monitor without a separate pass).

---

## §4 — Ranking logic (AC5)

Sort `ranked_companies` descending by:
1. `rollup_score` (desc)
2. tie → `term_match_count` (desc)
3. tie → `page_count_with_matches` (desc)
4. tie → `company_slug` (asc — stable deterministic)

`rank` = post-sort 1-indexed position. NO_PAGES / BLOCKED_UPSTREAM entries are INCLUDED in the ranking (score 0 typically) — not dropped — so the table is a complete 99-row universe view. This is the AC4 + AC8 "ranked_count: 99" requirement.

---

## §5 — data_quality_class derivation (AC4 + CVO §G1 overloaded-zero fix)

The CVO §G1 finding: an IR analyst handed a 0-score ranking cannot tell a true no-AM-signal zero from an upstream acquisition failure. consolidate sets `data_quality_class` per:

| Class | Predicate | Meaning |
|---|---|---|
| `SCORED` | `page_count_scanned > 0` AND score file present | Real score (incl. true-zero: pages crawled, no AM matches) |
| `BLOCKED_UPSTREAM` | gold/score.json carries an empty-body / blocked marker OR `page_count_scanned > 0 AND page_count_with_matches == 0 AND blocked-signal present` | Bronze EMPTY-BODY / silver BLOCKED record upstream (per v0.7.1 acquisition_failure_class) |
| `NO_PAGES` | `corp/{slug}/gold/web-scrape/{run-date}/score.json` MISSING (Stage 2 dispatch miss) | No bronze pages crawled |

NO_PAGES entries are synthesized for any universe slug whose score.json is absent (the consolidate Lambda knows the universe roster from the source-list / `serving/_meta/source-list-{date}.json`), so a Stage-2 dispatch miss surfaces as a flagged row rather than a silent gap.

---

## §6 — wm_classification handling (spec-LANDED v0.7.1 path)

The TO was authored when wm_classification was spec-pending. **Update: PRD v0.7.1 (`cba505dfb`) LANDED the present/adjacent/absent semantics**, and DS~B `score_web_gold.py` `.031` implements `classify_wm()`. So:

- **Primary path (read-through):** consolidate reads `wm_classification` directly from gold/score.json. DS~B's gold is the source-of-truth (classify_wm applies the v0.7.1 AND-gate at gold-tier).
- **Fallback path (derive):** if a gold/score.json predates `.031` and lacks `wm_classification` (only carries `rollup_score` + `class_diversity`), consolidate derives it from `scoring-weights-v0.2.json` `wm_classification_logic` block (which I authored):
  - present: `rollup_score >= 80 AND class_diversity >= 2`
  - adjacent: `(rollup_score >= 80 AND class_diversity < 2) OR (40 <= rollup_score < 80)`
  - absent: `rollup_score < 40`
  - null: score file unscoreable → carry `wm_classification_reason`
- **Consistency check:** if gold carries wm_classification AND the derive-path would disagree, consolidate logs a warning (gold-vs-config drift signal) but trusts the gold value (gold is authoritative; drift = a .031/config version-skew to surface to DS~B).

This dual-path makes consolidate robust to the gold-tier version-skew window during the .031 rollout.

---

## §7 — Top-5 signals (AC6)

Read the first 5 entries from `term_matches[]` in gold/score.json (already ordered by gold's per-match scoring). Preserve `{term, class, location_class, context_snippet}`. Decision-useful for IR-team spot-check ("why did this IMO rank high — what did the scraper actually find"). If `< 5` matches, take all available.

---

## §8 — History archive (AC7 + PRD Q-B)

Write BOTH:
- `serving/scoring.json` — overwrite-in-place (canonical live-served)
- `serving/_history/scoring/{run-date}.json` — append-by-date (per PRD v0.3 §3.2 Q-B ruling; scoring methodology changes are intentional + cite-able; history-class for scoring only)

Note path nuance: the TO says `serving/_history/scoring/{run-date}.json` while `.022 build_scoring_serving` uses `serving/_history/{run-date}/scoring_methodology.json`. These are distinct artifacts (ranked-table vs methodology) under the same `_history` root — no collision. Documented for AE IAM scope (`s3:PutObject serving/_history/scoring/*`).

---

## §9 — Lambda handler contract (AC3)

```
def lambda_handler(event, context):
    # event: {run_date, [universe_bucket], [output_bucket], [output_prefix]}
    # returns: {universe_size, scored_count, blocked_count, no_pages_count,
    #           ranked_count, output_key, started_at, ended_at, duration_ms}
```

Single-invocation per run-date (NOT per-IMO) per AC9. Reads via S3 list (`corp/*/gold/web-scrape/{run_date}/score.json`) + per-file get. Core transform (`consolidate(score_files, universe_roster, weights)`) is pure + unit-testable; the handler is a thin boto3 wrapper (same Storage-abstraction pattern as the .022 trio).

---

## §10 — Cost + sizing (AC9)

- Single invocation per run-date.
- Memory 512MB / timeout 5min initial (per TO recommendation) — 99 small JSON gets + in-memory sort + 2 puts; comfortably within.
- Reads gold (SSE-S3 baseline) + writes serving/* (KMS scope per PRD v0.4 §3.1 — Lambda role auto-gets `kms:GenerateDataKey` + `kms:Decrypt`). IAM: `s3:GetObject corp/*/gold/*` + `s3:PutObject serving/* + serving/_history/scoring/*`.

---

## §11 — Test plan (synthetic 5-IMO fixture; AC contract)

Unit tests against a synthetic 5-IMO gold fixture set covering all three data_quality classes + ranking + wm_classification dual-path:

| Fixture IMO | Shape | Asserts |
|---|---|---|
| `alpha` | SCORED present (rollup 90, class_diversity 3) | top rank; data_quality_class=SCORED; wm read-through=present |
| `beta` | SCORED adjacent (rollup 70) | mid rank; wm=adjacent |
| `gamma` | SCORED true-zero (page_count_scanned>0, matches=0, rollup 0) | data_quality_class=SCORED (NOT blocked); wm=absent |
| `delta` | BLOCKED_UPSTREAM (empty-body marker) | data_quality_class=BLOCKED_UPSTREAM; ranked not dropped |
| `epsilon` | NO_PAGES (score.json absent; in roster) | synthesized row; data_quality_class=NO_PAGES; score 0 |

Plus: ranking tie-break order; wm derive-fallback path (gold lacking wm_classification); wm gold-vs-derive drift warning; top-5 truncation; distribution aggregates; ranked_count == universe_size.

Target ~15-20 tests (more transform surface than the .022 skeletons — derivation + classification + tie-break + roster-synthesis branches).

---

## §12 — Sequencing + open items

- **GATE:** AC8 empirical run blocks on FIND_INSURE.008 AC7 (99 gold/score.json files exist). Design + code (this brief + consolidate_scoring.py + tests) pre-stage NOW.
- **wm_classification** spec landed (v0.7.1) — design encodes read-through-primary + derive-fallback. No longer a blocker.
- **.021 IR-team feedback protocol** — serving/scoring.json is .021's input contract; no breaking schema changes without .021 sign-off (schema-stability discipline).
- **AE 0.7 deploy** — source-ship triggers AE deploy cycle; comp-iam confirmation post-deploy.
- **Open Q for ws COO/CTO (non-blocking):** should `serving/scoring.json` (this .023 web-scrape consolidation) eventually merge with `serving/companies.json` (.022 full company join) at Phase 3 convergence? v0.1 keeps separate per TO scope. Flag for Phase-3-close architecture review.

— 0.1.0_DS_MarketIntelligence~E 2026-05-28 (FIND_INSURE.023 pre-stage design v0.1)
