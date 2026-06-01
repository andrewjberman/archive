# /verify-channel Mode A (surface-level) — MDPF inflection re-emit — 2026-06-01T1329Z

**Verdict: PASS** (1 honest-limit NOTE, non-blocking)
**Requester:** DS~B (`0.4.0_DS_ClientPlatform~B`) `[VERIFY-CHANNEL ASK]` 1325Z; COO pre-SYNC 1318Z. Verdict gates inflection matrix-cell flip → confirmed + feeds COO RAVC2 close.
**Verifier≠fixer:** DS~B fixed (re-emit + guard `a9352506f`); CVO independent-verifies. Satisfied.
**Artifact:** `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json` (CloudFront-served; one JSON/date). All reads are independent S3 pulls, not self-report.

## Defect under repair
5/29 backfill re-emit used `build_mdpf_process_backfill.py` (49F-only pre-onboard tool) over post-onboard dates 5/18–5/29, dropping Inflection partner from 8 served artifacts → global understated by inflection-2a (~$96M), inflection segment panel empty.

## 4-point verify (COO/DS~B spec) → 4-check + sharp-structural method

### Point 1 — Inflection partner present on all 8 re-emitted dates (+ untouched 5/21, 5/28) — **PASS**
All 8 re-emitted (5/18,19,20,22,25,26,27,29) + 2 controls (5/21,5/28): `partners[] = ['49financial','inflection']`. `sentinel_2_partners_present.status = PASS` on every checked date (`missing: []`). `overall = PASS` on all.
- FRESH: 8 re-emitted LastModified = **2026-06-01 13:22–13:23 GMT** (today's re-emit). Controls 5/21 (21-May 15:03) + 5/28 (28-May 15:03) **untouched** → re-emit write-scope was exactly the 8, not the controls.

### Point 2 — 49financial intact (not regressed) — **PASS**
`49financial.total_aua` ~$1.65–1.69B, smooth + continuous across the untouched-control→re-emit boundary: 5/21 control $1,651,107,904 → 5/22 re-emit $1,671,659,642 → … → 5/28 control $1,693,428,396 → 5/29 $1,687,171,122. No discontinuity at the re-emit seam.

### Point 3 — Global corrected to include 2a (~+$96M) — **PASS** (sharp reconciliation, not identity-gate trust)
GLOBAL = `aggregate.opal_aggregate_aua` = 1a+1b+1c+2a (per audit: includes inflection MODELS, excludes 2b non-model). Independently computed `49f_total + inflection.model_aua(2a)` per date — matches `global_agg` **to the cent** on all checked dates:
| Date | 49f_total | infl 2a (model_aua) | computed sum | global_agg | match |
|---|---|---|---|---|---|
| 5/29 | 1,687,171,121.54 | 96,601,199.67 | 1,783,772,321.21 | 1,783,772,321.21 | ✓ (= DS~B-stated figure) |
| 5/28 (ctrl) | 1,693,428,396.35 | 96,211,989.78 | 1,789,640,386.13 | 1,789,640,386.13 | ✓ |
| 5/19,20,25,27 | — | — | — | — | ✓ all MATCH to cent |
infl 2a progression 93.6M (5/18) → 96.6M (5/29), smooth. infl total (2a+2b) 5/28 = $203.98M (= audit $204M). **Not identity-masking** — per-component values individually plausible + continuous across boundary.
- DS~B caveat confirmed: corrected 5/29 global $1,783.77M < bad-49F-only $1,847.97M because the bad backfiller used a different (inflated) 49f basis; canonical+sentinels are system-of-record, and the canonical value reconciles internally to the cent.

### Point 4 — NO 12/26 (Dec) F4-reclass regression — **PASS** (sharp cross-partition disjointness)
12/26 partition (`2025-12-26.json`): LastModified = **29-May 19:36 GMT (F4-patch era), NOT 2026-06-01** — re-emit never wrote it. Corroborating: `methodology_version = v0_9` (F4-patch vintage) vs canonical-aggregator methodology on the May re-emit. Still `partners=['49financial','inflection']`, `overall=PASS`, global=$1,335,552,884.78. F4 patch `f44ab785d` untouched. Disjointness verified at partition-write + methodology-vintage level, not assumed.

## Step 3.5 — decision-useful / NOTE (honest-limit, non-blocking)
**NOTE — 5/26 and 5/27 carry identical values** (global $1,779,865,325.21, infl 2a $95.64M, 49f identical on both). Both dates are structurally correct (both partners, reconcile to cent, overall PASS). This is a **pre-existing upstream model_aua-feed carry-forward** (5/27 trading day with no fresh feed delta vs 5/26), **NOT introduced by this re-emit** — the canonical aggregator faithfully aggregated whatever source feed existed per date. Out of scope for THIS fix (inflection-restoration is correct on both). Flagged for DS~B/COO disposition as a separate upstream-freshness question (whether 5/27 should carry 5/26's feed); a daily-trend chart would render a flat 5/26→5/27 step.

## Routing
PASS → DS~B (requester) + CC COO (RAVC2 close consumer). Gates inflection matrix-cell → confirmed. NOTE routed same; non-blocking.
