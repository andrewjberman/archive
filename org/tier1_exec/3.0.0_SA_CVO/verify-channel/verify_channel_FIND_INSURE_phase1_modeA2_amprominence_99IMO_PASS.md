# /verify-channel — FIND_INSURE Phase 1 Mode A#2: am_prominence scoring-correctness (99-IMO cohort)

**Verifier:** 3.0.0_SA_CVO (ws CVO) — independent (verifier ≠ fixer; I authored no scoring code).
**Mode:** A (surface-level), the am_prominence scoring-correctness leg gating Phase 1 RAVC2-Accept.
**Trigger:** COO `[VERIFY-ELIGIBLE-COHORT]` 11:47Z + DS coverage 99/99 BARS_MET (Class 1 closeout).
**Cohort:** 99 IMOs, gold `corp/{slug}/gold/web-scrape/2026-05-27/score.json`, bucket `opal-data-imo`.
**Verdict time:** 2026-05-28T12:40Z.
**Input (not replacement):** aggregator `Temp/find_insure_agg_2705_1142Z.json` (DS coverage authority). My binding evidence = independent boto3 S3 read of all 99 gold records + content-hash + classifier recompute.

---

## VERDICT: PASS (CORROBORATE) — am_prominence dual-bar is correct and generalizes at universe scale.

Phase 1 RAVC2-Accept is cleared on the scoring-correctness leg. One explicit decision-useful **observation** (non-blocking) recorded below for an eyes-open close-out.

| Axis | Verdict | Evidence |
|---|---|---|
| Mechanical (4-check) | GREEN | EXISTS 99/99 (0 missing); FRESH (LastModified all 2026-05-28 05:50–06:22Z, single run window); SCALED 99/99; NOT-FROZEN (99 distinct ETags / 99); taxonomy_version=**v3 on all 99**; rollup_score **0-mismatch** vs aggregator |
| Structural (sharp test) | GREEN | wm_classification **recomputed from raw components for all 99 → 0 mismatch** vs emitted (deployed classifier == spec logic); dual-bar discriminates (below) |
| Decision-useful (Step 3.5) | GREEN + observation | Output genuinely discriminates; 52 nulls are honest unrecoverable-tail; effective yield 47/99 noted |
| Constitution-coherence (e) | NULL | Mode A surface-level leg; (e) subscan fires on Mode B comprehensive only |

---

## Sharp structural test — dual-bar generalization (the core mandate)

`am_prominence = high_signal_AM_weight / (high_signal_AM_weight + annuity_baseline_weight)`; T_present = 0.50.

**TP-preserve — 7 "present", all valid** (every one amp≥0.50 AND high_signal_weight>0; zero logic violations):

| slug | amp | rollup | hs_wt | ann_wt |
|---|---|---|---|---|
| avantax-wealth-management | 1.0 | 100 | 36.34 | 0.0 |
| futurity-first | 1.0 | 76 | 2.55 | 0.0 |
| pacific-capital-resource-group | 1.0 | 100 | 16.0 | 0.0 |
| preferred-marketing-associates | 1.0 | 100 | 27.85 | 0.0 |
| the-retirement-network | 0.98 | 63 | 48.45 | 1.0 |
| lincoln-investment | 0.94 | 100 | 95.0 | 5.9 |
| gradient-financial-group | 0.68 | 42 | 75.5 | 35.2 |

**TN-suppress — the v0.7.1 FP regression is fixed** (high rollup_score, annuity-dominated → correctly NOT present):

| slug | rollup | amp | hs_wt | ann_wt | class |
|---|---|---|---|---|---|
| allianz-life | 100 | 0.0117 | 8.8 | 748.5 | (suppressed) |
| eagle-strategies | 100 | 0.0327 | 11.5 | 340.7 | (suppressed) |
| senior-market-sales | 100 | 0.3443 | 183.0 | 348.6 | adjacent |
| national-life-group | 86 | 0.0274 | 20.0 | 710.8 | (suppressed) |
| midland-national | 85 | 0.0482 | 23.7 | 468.4 | (suppressed) |
| metlife | 66 | 0.0020 | 0.75 | 370.8 | (suppressed) |
| integrity-marketing-group | 56 | 0.1311 | 3.2 | 21.2 | adjacent |

**No calibration drift:** the 0.50 threshold cleanly separates two well-formed clusters — present cluster amp ∈ [0.68, 1.0], suppressed/annuity cluster amp ∈ [0.002, 0.34]. The ratio decouples raw AM-vocab magnitude (rollup) from genuine AM-transition prominence exactly as designed. fp_rate on the annuity-carrier class = 0.

---

## Decision-useful (Step 3.5) — completion-matrix + unrecoverable-tail null-accounting

wm_classification distribution across 99: **present 7 / adjacent 17 / absent 23 / null 52.**

All 52 nulls = reason `blocked_upstream`. Root-caused (broken-compute-vs-absent-data discriminator):
- silver reasons: parked-or-404 **26**, robots **19**, cert-failure **4**, empty-body **2**, none 1
- blocked-IMO bronze content: **median 0 KB** (max 1.8 KB) vs classified-IMO **median 1,520 KB**

→ Resolves decisively to **absent data, not broken compute**: these sites actively block (robots.txt) or do not exist as scrapable sites (parked / 404 / cert-fail). The null+`blocked_upstream` is the correct honest handling — score-web refuses to fabricate a classification from a block page. This is the "unrecoverable-tail null-accounting" the mandate anticipated.

**Observation (non-blocking, for eyes-open close-out):** effective classification yield = **47/99** (52 honest nulls). Read "BARS_MET 99/99" as *gold-files-present*, NOT 99 usable classifications. Expected per the unrecoverable-tail design; surfaced so RAVC2-Accept + the Andrew chain are made knowingly. Not a scoring defect; not a coverage anomaly — a real-world property of scraping a public IMO list. Future-phase candidate: a recovery pass on the 19 robots-blocked (policy, not absence) is the only sub-segment with any recoverability.

---

## Verifier-purity statement
DS attests coverage + cascade-integrity (rollup_score axis); I attest scoring-correctness (am_prominence dual-bar). Independently confirmed same-artifact (rollup_score 0-mismatch), different meaning. My read was the 2026-05-27 partition (not the empty today-default partition that produced the false "12/99"). No self-validation surface — I authored no FIND_INSURE scoring code.

## Routing
PASS → COO (requester) + CC CTO (ratifies RAVC2-Accept) + DS base + MSTR. No REPAIR-AMENDMENT (no mechanical-untruth, no coverage-gap; the yield observation is design-expected, not an inadequate-coverage finding).
