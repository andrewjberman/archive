# /verify-channel (Mode A surface-level) — ADHC_BDTSCLB.001 AC4 bd served-parity

**CVO:** 3.0.0_SA_CVO · **Time:** 2026-06-03T17:17Z
**Trigger:** 0.6.0_AE [GO] 170842Z — full bd publish complete (chain_full_20260603_153157.log finished 16:48:06Z, phases A→D4, instance self-terminated 16:49Z).
**Gate:** CTO mandatory close-gate — served `platinum/advisors/{id}/timeseries.json` retains ALL advisors/dates/rich fields (`total_aua_fee_paying/_no_fee` + `nna_canonical_fee_paying`) matching D_02 AFTER the publisher single-writer removal (bd-v2.25.0); nothing dropped.
**Method:** independent full-set artifact read (boto3) of live PROD served + D_02 gold. Verifier≠fixer (0.6.0 shipped + ran; I verify independently, not their summary).

## Verdict: PASS (GREEN). AC4 met — D_02 sole-writer served set complete + correct; no-clobber structurally double-guaranteed.

### Core checks (full 169-advisor served set)
- **EXISTS/FRESH:** 165/169 served advisors rewritten by today's publish (LastModified ≥ 16:40Z); 0 empty.
- **RICH FIELDS:** 165/165 fresh advisors carry `total_aua_fee_paying`, `total_aua_no_fee`, `nna_canonical_fee_paying`.
- **RECONCILE (sharp):** `total_aua_fee_paying + total_aua_no_fee == total_aua` to-the-cent on **all 165 — 0 reconcile failures** (tol 0.01).
- **PARITY vs D_02 (D_04 pass-through):** spot-checked abby_horton (served 763 == gold 763 dates, last-row money fields byte-match) + grant_boren (last-row money fields match: tap=160,440,249.94 both). D_04 bridges D_02 faithfully.
- **SET PARITY:** served current-book set == D_02-book-enumerated set. (D_02 gold has 185 advisor DIRS vs 169 served — the 18 extra are timeseries-only / NO book.json; D_04 enumerates from book.json by design, so they're legitimately not served. This is the TO coverage proof's "served == D_02 set" stated precisely as "== D_02-book set.")

### The 4 apparent parity exceptions — RESOLVED as pre-existing orphans (NOT a fix-caused drop)
`49f_house`(served 4/9), `unassigned`(4/9), `unknown`(4/9), `dominic_depizzol`(served 5/26) lack the W2b fields because their served copies are STALE (predate W2b emit) — and **all 4 have NO current book.json**, so D_04 correctly does not refresh them (not in current enumeration). Their stale dates (4/9, 5/26) PRE-DATE the bd-v2.25.0 change (6/3) by weeks/months → these are pre-existing orphan served artifacts, untouched by and unrelated to the single-writer removal. `unassigned`/`unknown` are served-only catch-alls (absent from D_02 gold entirely).

### No-clobber — double-structural (independently corroborated)
(a) Publisher's `build_advisor_timeseries` writer REMOVED from code (bd-v2.25.0; I confirmed the function is gone from the deployed publisher earlier this session). (b) 0.6.0 exercised the publisher directly 16:54Z → FATAL at load_sources (`pyarrow ArrowInvalid: No match for FieldRef.Name(nna)` — account_performance.parquet no longer materializes `nna`, which D_02 derives) → wrote nothing (book.json mtime + timeseries sha unchanged). Pre-existing (publisher dormant ~2 months, last ~2026-04-07), not caused by bd-v2.25.0. Net: served timeseries is produced SOLELY by D_02→D_04; the "publisher overwrites" path is moot (writer removed AND publisher crashes pre-write). 0.6.0's crash evidence accepted as corroborating; the code-removal alone is the primary guarantee, which I independently confirmed.

## Observations (non-blocking, pre-existing, NOT AC4 regressions — routed for awareness)
1. **Orphan stale served artifacts** — 4 advisors no-longer-in-current-book retain stale served timeseries.json (D_04 doesn't clean up served artifacts when an advisor leaves the book). Pre-existing D_04 hygiene gap; low real-world impact (portal enumerates current roster, not the served-bucket listing). Route DS/AE (D_04 owner) as P3 hygiene.
2. **D_04 serves a history window vs gold full-history** — grant_boren served 1094 dates vs D_02 gold 2157 (abby_horton 763==763, no window needed). By-design D_04 lookback (~3y), unchanged by bd-v2.25.0. Not a drop.

## Disposition
AC4 = **PASS**. Last binding close-gate on ADHC_BDTSCLB.001 single-writer hardening met. Verdict → CTO + COO + 0.6.0. The 2 observations are pre-existing/separate; P3 hygiene to D_04 owner if desired, not closure-blocking.
