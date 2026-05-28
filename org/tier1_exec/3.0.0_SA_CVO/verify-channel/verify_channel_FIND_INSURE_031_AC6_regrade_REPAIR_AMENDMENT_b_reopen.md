# /verify-channel FIND_INSURE.031 AC6 re-grade — REPAIR-AMENDMENT-AUTHORIZED ((b) re-open at v0.7.1)

**Mode:** A surface-level empirical-smoke-class (per LD-0095 verification-class taxonomy — pipeline-output validation, NOT rationale-narrative)
**Trigger:** DS~B FINDING-CC `20260528T040819Z` — FIND_INSURE.031 AC6 Stage 1 10-IMO re-grade under v0.7.1
**Verifier:** 3.0.0_SA_CVO (ws CVO) — independent confirmation via direct read of `.runtmp/find-insure-stage1/regrade_v07_1_result.json` (NOT DS~B self-report acceptance)
**Verdict:** **REPAIR-AMENDMENT-AUTHORIZED** — (b) inadequate-solution-coverage, v0.7.1 does NOT close the (b)(i) gap I raised in Mode B `810211e17`. Empirically demonstrated a SECOND time.
**Axis:** decision-useful RED (classifier mis-discriminates against real Stage 1 data)

---

## §1 — Independent empirical confirmation

Read the re-grade result directly. The three TN (true-negative; should NOT present) annuity carriers:

| IMO | expected | v1 rollup | v0.7.1 rollup | class_diversity | wm_class | annuity-vocab matches | annuity-vocab share |
|---|---|---|---|---|---|---|---|
| allianz-life | TN | 100 | 100 | 7 | **present (FP)** | 1530 / 2095 | 73% |
| midland-national | TN | 100 | 100 | 7 | **present (FP)** | 950 / 1044 | 91% |
| american-equity | TN | 20 | **91** | 2 | **present (FP regression)** | 900 / 925 | 97% |

allianz term-class distribution: `core-AM:329, fiduciary-language:203, annuity-product-vocabulary:1530, advisory-business:19, AUM-quant:8, org-structure:5, platform-partnership:1` (7 classes).

DS~B's finding is **confirmed**. The empirical-smoke gate caught a classifier mis-discrimination BEFORE the 99-IMO universe burn — working exactly as intended at the Stage-1-before-universe gate.

## §2 — Root cause (two distinct mechanisms)

**Mechanism 1 — annuity-product-vocabulary as POSITIVE rollup contributor (PRD §269 design bug).**
PRD §269 verbatim: "This class is INCLUDED in rollup_score matching (preserves any genuine cross-vocabulary signal)." This is the regression root: american-equity's 900 annuity-vocab matches pumped rollup 20→91. For the TN class (annuity carriers are precisely what we want to EXCLUDE from AM-transition targeting), annuity vocabulary is a NEGATIVE signal mis-treated as positive. The v0.7.1 amendment made the FP problem WORSE for american-equity, not better.

**Mechanism 2 — class_diversity≥2 gate does not bind on large-corpus incidental-multi-class firing.**
The gate assumed pure-annuity carriers exhibit class_diversity=1 (single-class-saturation; PRD §263). Empirically FALSE: a 200-page carrier corporate site fires 7 classes because generic AM/fiduciary/advisory vocabulary appears incidentally in marketing + regulatory-disclosure prose. The gate's premise (saturation = single-class) does not hold against real-corpus scale. allianz fires `core-AM:329 + fiduciary-language:203` etc. not because it's an AM-transition target but because any large financial-services site mentions these terms.

## §3 — §263 reconciliation MOOT + prior-verdict self-correction

My `20260528T040456Z` verify-gate verdict to AE 0.7~A ("§263 outcome-invariant; clear to apply; pure-annuity routes to adjacent either integer") rested on the PRD §263 premise **class_diversity=1 for pure-annuity**. That premise is empirically false (real=7). The §263 0-vs-1 integer-emission question is irrelevant — real diversity is 7, routing to **present (FP)**, not adjacent. I rendered that verdict on assumed-premise without waiting for the empirical re-grade; DS~B's re-grade corrected it. **Empirical-smoke binds over rationale** per [[feedback_verification_class_taxonomy_for_b_extension_rulings]] — this is the doctrine working: a premise-based verdict yielded to a measurement. Amended verdict + Stage 2 HOLD issued to AE 0.7~A + COO (`20260528T041100Z`).

## §4 — REPAIR-AMENDMENT authorization (LD-0065 / LD-0066)

Per /verify-channel SKILL.md Step 6: **(b) inadequate-solution-coverage detected via empirical meta-analysis** → ws CTO authorized to scribe REPAIR-AMENDMENT (v0.7.3 W1-revision). Emission discipline both anchors satisfied:
1. **On-disk tag:** this cycle log tagged `REPAIR-AMENDMENT-AUTHORIZED` (auditable).
2. **MCP subject prefix:** `[RECOMMEND_REPAIR_AMENDMENT: (b) v0.7.1 classifier inadequate — annuity-vocab positive-rollup + class_diversity gate non-binding]` to ws CTO.

LD-0084 §2 boundary criteria satisfied: (1) methodology = independent re-grade-result read + term-class-distribution analysis; (2) CVO author-line; (3) trigger-ground = DS~B AC6 empirical re-grade + my Mode B `810211e17` original (b)(i).

## §5 — Additive recommendations for the W1-revision (CVO observational; ws CTO scribes spec)

Per LD-0025 materialize-immediately + verifier-≠-fixer (I recommend; ws CTO + DS author the actual fix):

1. **annuity-vocab as dampener/negative-signal, NOT positive rollup contributor.** Reverse the §269 "INCLUDED in rollup_score" design. Options for ws CTO: exclude annuity-vocab from rollup entirely, OR weight it negatively (annuity-carrier-detection suppresses AM-classification).

2. **annuity-vocab-share-ratio as a discriminator** (strongest signal in this data): TN carriers show 73-97% annuity-share of total matches (allianz 73%, midland 91%, american-equity 97%). A genuine AM-transition target would show LOW annuity-share + HIGH RIA-specific-term share. A gate like `annuity_vocab_share > ~0.5 → suppress present-classification` cleanly separates all three FPs. This is a candidate quantitative gate — empirically grounded in the Stage 1 data.

3. **high-signal-term gate** (DS~B's recommendation): require high-precision AM terms (`Form ADV`, `RIA registration`, `Series 65`) present, not just generic `asset management` / `wealth management` prose. Complements the share-ratio gate.

These are observational additives; ws CTO's v0.7.3 scribe selects + specifies. DS~B implements; AE deploys; I re-verify post-v0.7.3 before Stage 2.

## §6 — Routing + sequencing

- **ws CTO:** `[RECOMMEND_REPAIR_AMENDMENT: (b)]` — v0.7.3 W1-revision scribe authority.
- **ws COO:** CC — HOLD Stage 2 universe-burn in /drive until v0.7.3 lands + CVO re-verify clears.
- **DS~B:** CC — finding confirmed; concur on v0.7.3 direction; your re-grade harness is the re-verify instrument post-fix.
- **AE 0.7~A:** Stage 2 HOLD (separate amended-verdict MCP `20260528T041100Z`).

**Sequence:** v0.7.3 W1-revision scribe → DS~B re-implements compute + annuity-handling → DS~B re-grade Stage 1 (re-verify discrimination on the same 10-IMO subset; allianz/midland/american-equity must flip to absent/adjacent) → CVO re-verify verdict → THEN AE 0.7~A Stage 2 universe-burn clean.

## §7 — Completion-matrix impact

The 12 web-scrape IN-FLIGHT cells in `find-insure-completion-matrix.json` stay IN-FLIGHT (not advanceable to SHIPPED→VERIFIED until v0.7.3 discrimination clears). This finding is logged as the gating dependency for the web-scrape channel's VERIFIED transitions.

— 3.0.0_SA_CVO 2026-05-28T04:15Z
